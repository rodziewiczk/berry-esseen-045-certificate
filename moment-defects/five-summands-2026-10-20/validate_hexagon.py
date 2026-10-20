#!/usr/bin/env python3
"""Static TeX preflight and optional single-source Hexagon packaging.

This program never compiles TeX, executes a proof, accesses the network, or
changes the manuscript. Without --package it performs read-only checks.
The checks are deliberately syntactic, not a mathematical or TeX-engine audit.
"""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import io
import json
from pathlib import Path
import re
import sys
import zipfile


WORKSPACE = Path(__file__).resolve().parents[2]
MAX_SOURCE_BYTES = 16 * 1024 * 1024
ENTRY_NAME = "manuscript.tex"
REFERENCE_COMMANDS = {
    "ref", "eqref", "pageref", "autoref", "cref", "Cref", "vref", "Vref",
    "nameref",
}
CITATION_COMMANDS = {"cite", "citep", "citet", "citealp", "citealt", "nocite"}
EXTERNAL_FILE_COMMANDS = {
    "input", "include", "includeonly", "includegraphics", "graphicspath",
    "bibliography", "bibliographystyle", "addbibresource", "externaldocument",
    "verbatiminput", "VerbatimInput", "lstinputlisting", "inputminted",
    "includepdf", "includeinkscapegraphics", "subfile", "subimport", "import",
    "InputIfFileExists", "IfFileExists", "openin", "openout", "read", "write",
    "ShellEscape",
}
COMMAND = re.compile(r"\\([A-Za-z@]+|.)", re.DOTALL)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_bounded(path: Path, limit: int = MAX_SOURCE_BYTES) -> bytes:
    with path.open("rb") as stream:
        data = stream.read(limit + 1)
    if len(data) > limit:
        raise ValueError(f"File exceeds the {limit}-byte safety limit: {path}")
    return data


def strip_comments(text: str) -> str:
    """Remove TeX comments, retaining line breaks and escaped percent signs."""
    output = []
    for line in text.splitlines(keepends=True):
        cut = len(line)
        for index, char in enumerate(line):
            if char != "%":
                continue
            preceding_slashes = 0
            position = index - 1
            while position >= 0 and line[position] == "\\":
                preceding_slashes += 1
                position -= 1
            if preceding_slashes % 2 == 0:
                cut = index
                break
        if cut == len(line):
            output.append(line)
        else:
            ending = "\r\n" if line.endswith("\r\n") else "\n" if line.endswith("\n") else ""
            output.append(line[:cut] + ending)
    return "".join(output)


def skip_space(text: str, position: int) -> int:
    while position < len(text) and text[position].isspace():
        position += 1
    return position


def read_group(text: str, position: int, left: str, right: str):
    """Read one balanced group, treating escaped delimiters as ordinary text."""
    position = skip_space(text, position)
    if position >= len(text) or text[position] != left:
        return None, position
    start = position + 1
    depth = 1
    position = start
    while position < len(text):
        char = text[position]
        if char == "\\":
            position += 2
            continue
        if char == left:
            depth += 1
        elif char == right:
            depth -= 1
            if depth == 0:
                return text[start:position], position + 1
        position += 1
    raise ValueError(f"Unclosed {left}{right} group at character {start - 1}")


def command_argument(text: str, position: int):
    position = skip_space(text, position)
    if position < len(text) and text[position] == "*":
        position += 1
    while True:
        option, next_position = read_group(text, position, "[", "]")
        if option is None:
            break
        position = next_position
    return read_group(text, position, "{", "}")


def duplicates(values: list[str]) -> list[str]:
    return sorted(key for key, count in Counter(values).items() if count > 1)


def normalize_whitespace(text: str) -> str:
    return " ".join(text.split())


def inspect_source(data: bytes, abstract_data: bytes | None = None) -> dict:
    text = strip_comments(data.decode("utf-8-sig"))
    labels: list[str] = []
    references: list[str] = []
    bibitems: list[str] = []
    citations: list[str] = []
    external = []
    malformed = []
    environments = {"document_begin": 0, "document_end": 0}
    for match in COMMAND.finditer(text):
        name = match.group(1)
        if name in EXTERNAL_FILE_COMMANDS:
            external.append({"command": "\\" + name, "line": text.count("\n", 0, match.start()) + 1})
        if name not in REFERENCE_COMMANDS | CITATION_COMMANDS | {"label", "bibitem", "begin", "end"}:
            continue
        argument, _ = command_argument(text, match.end())
        if argument is None:
            malformed.append({"command": "\\" + name, "line": text.count("\n", 0, match.start()) + 1})
            continue
        if name == "label":
            labels.append(argument.strip())
        elif name == "bibitem":
            bibitems.append(argument.strip())
        elif name in REFERENCE_COMMANDS:
            references.extend(key.strip() for key in argument.split(","))
        elif name in CITATION_COMMANDS:
            citations.extend(key.strip() for key in argument.split(","))
        elif argument == "document":
            environments["document_begin" if name == "begin" else "document_end"] += 1

    abstracts = re.findall(r"\\begin\s*\{abstract\}(.*?)\\end\s*\{abstract\}", text, re.DOTALL)
    abstract_check = {"present_count": len(abstracts), "comparison_requested": abstract_data is not None}
    if abstract_data is not None:
        supplied = strip_comments(abstract_data.decode("utf-8-sig"))
        abstract_check["normalized_equal"] = (
            len(abstracts) == 1
            and normalize_whitespace(abstracts[0]) == normalize_whitespace(supplied)
        )

    checks = {
        "labels": len(labels),
        "references": len(references),
        "missing_references": sorted(set(references) - set(labels)),
        "duplicate_labels": duplicates(labels),
        "bibitems": len(bibitems),
        "citations": len(citations),
        "missing_citations": sorted(set(citations) - set(bibitems) - {"*"}),
        "duplicate_bibitems": duplicates(bibitems),
        "unused_bibitems": sorted(set(bibitems) - set(citations)),
        "external_file_commands": external,
        "malformed_checked_commands": malformed,
        "empty_label_or_reference_or_citation": "" in labels + references + bibitems + citations,
        **environments,
        "abstract": abstract_check,
    }
    failures = []
    for key in ("missing_references", "duplicate_labels", "missing_citations", "duplicate_bibitems", "external_file_commands", "malformed_checked_commands", "empty_label_or_reference_or_citation"):
        if checks[key]:
            failures.append(key)
    if environments != {"document_begin": 1, "document_end": 1}:
        failures.append("document_environment_count")
    if len(abstracts) != 1:
        failures.append("abstract_environment_count")
    if abstract_data is not None and not abstract_check["normalized_equal"]:
        failures.append("abstract_mismatch")
    return {"passed": not failures, "failures": failures, "checks": checks}


def make_source_zip(source: bytes) -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        entry = zipfile.ZipInfo(ENTRY_NAME, date_time=(2026, 10, 20, 0, 0, 0))
        entry.compress_type = zipfile.ZIP_DEFLATED
        entry.create_system = 3
        entry.external_attr = 0o100644 << 16
        archive.writestr(entry, source, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    result = buffer.getvalue()
    verify_source_zip(result, source)
    return result


def verify_source_zip(data: bytes, source: bytes) -> None:
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        if archive.namelist() != [ENTRY_NAME]:
            raise ValueError("ZIP must contain exactly one root-level manuscript.tex")
        if archive.read(ENTRY_NAME) != source or archive.testzip() is not None:
            raise ValueError("ZIP source bytes or CRC do not match the saved manuscript")


def ensure_new_or_identical(path: Path, expected: bytes) -> None:
    if path.is_symlink():
        raise ValueError(f"Refusing symlink destination: {path}")
    if path.exists() and (not path.is_file() or read_bounded(path) != expected):
        raise ValueError(f"Refusing to overwrite a different existing destination: {path}")


def write_new_or_identical(path: Path, data: bytes) -> str:
    ensure_new_or_identical(path, data)
    if path.exists():
        return "already_identical"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as stream:
        stream.write(data)
    if read_bounded(path) != data:
        raise ValueError(f"Written file failed byte verification: {path}")
    return "created"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=WORKSPACE / "manuscript/drafts/appendix_elementary_045.tex")
    parser.add_argument("--abstract-file", type=Path, help="Optional UTF-8 file containing the exact abstract body; comparison normalizes whitespace only")
    parser.add_argument("--package", action="store_true", help="Explicitly create the source copy and source-only ZIP after successful checks")
    parser.add_argument("--stage-source", type=Path, default=WORKSPACE / "output/hexagon_2026-10-20/manuscript.tex")
    parser.add_argument("--zip-path", type=Path, default=WORKSPACE / "output/berry_esseen_hexagon_2026-10-20_sources.zip")
    args = parser.parse_args()
    report = {
        "operation": "package" if args.package else "read_only_validation",
        "source": str(args.source.resolve()),
        "scope": "Static source and packaging checks only; no TeX compilation or mathematical verification",
        "manual_mathematical_metadata_checks": [
            "Verify that the abstract states C5 <= CE, not strict C5 < CE, unless separately proved.",
            "Verify that any all-index conclusion and any range n >= 6 visibly retain their precise conditional premises.",
        ],
    }
    try:
        source = read_bounded(args.source)
        abstract = read_bounded(args.abstract_file) if args.abstract_file is not None else None
        report.update({"source_bytes": len(source), "source_sha256": sha256(source)})
        report.update(inspect_source(source, abstract))
        if not report["passed"]:
            print(json.dumps(report, ensure_ascii=False, indent=2))
            return 1
        if args.package:
            if args.stage_source.absolute() == args.zip_path.absolute():
                raise ValueError("Stage source and ZIP destinations must be different")
            package = make_source_zip(source)
            # Check both destinations before creating either output.
            ensure_new_or_identical(args.stage_source, source)
            ensure_new_or_identical(args.zip_path, package)
            if read_bounded(args.source) != source:
                raise ValueError("Manuscript changed during validation; retry with the saved final source")
            report["staged_source"] = {
                "path": str(args.stage_source.resolve()),
                "status": write_new_or_identical(args.stage_source, source),
                "sha256": sha256(source),
            }
            report["source_zip"] = {
                "path": str(args.zip_path.resolve()),
                "status": write_new_or_identical(args.zip_path, package),
                "bytes": len(package),
                "sha256": sha256(package),
                "entries": [ENTRY_NAME],
                "contains_pdf_or_lean_or_data": False,
            }
            verify_source_zip(read_bounded(args.zip_path), source)
            if read_bounded(args.source) != source:
                raise ValueError("Manuscript changed during packaging; outputs reflect the reported source SHA256, not the newer source")
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0
    except (OSError, UnicodeError, ValueError, zipfile.BadZipFile) as error:
        report.update({"passed": False, "error": str(error)})
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 2


if __name__ == "__main__":
    sys.exit(main())
