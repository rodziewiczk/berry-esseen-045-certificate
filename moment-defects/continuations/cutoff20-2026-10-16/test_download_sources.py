"""Tiny, offline transport/extraction tests; no mathematical checker is run.

Run with ``python -B test_download_sources.py`` from this directory. All
payloads are generated inside TemporaryDirectory, and every network call is
mocked or forbidden. The large-archive budget test uses metadata only.
If the operating-system TEMP is sandbox-restricted, set CUTOFF20_TEST_TMPDIR
to an existing writable scratch directory before running these tests (for
example in PowerShell: $env:CUTOFF20_TEST_TMPDIR='C:/path/to/workspace/tmp').
"""
from __future__ import annotations

import contextlib
import hashlib
import io
import os
from pathlib import Path
import tempfile
import unittest
from unittest import mock
import zipfile

import download_sources as helper


class DownloadSourcesTests(unittest.TestCase):
    MAX_FIXTURE_BYTES = 32 * 1024

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(
            prefix="cutoff20-helper-unit-", dir=os.environ.get("CUTOFF20_TEST_TMPDIR")
        )
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        self.no_network = mock.patch.object(
            helper.urllib.request,
            "urlopen",
            side_effect=AssertionError("A unit test attempted real network access"),
        )
        self.no_network.start()
        self.addCleanup(self.no_network.stop)
        self.disk_space = mock.patch.object(
            helper.shutil, "disk_usage", return_value=mock.Mock(free=256 * 1024**2)
        )
        self.disk_space.start()
        self.addCleanup(self.disk_space.stop)

    def archive(self, entries, filename="tiny.zip"):
        path = self.base / filename
        with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_STORED) as archive:
            for name, data in entries:
                archive.writestr(name, data)
        self.assertLessEqual(path.stat().st_size, self.MAX_FIXTURE_BYTES)
        return path

    def entry(self, path, **changes):
        result = {
            "name": path.name,
            "bytes": path.stat().st_size,
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        }
        result.update(changes)
        return result

    def manifest(self):
        return {"repository": "example/project", "release_tag": "unit-test"}

    def rejected_extraction(self, entries):
        path = self.archive(entries)
        destination = self.base / "new-output"
        with self.assertRaises(ValueError):
            helper.extract_isolated(path, destination)
        self.assertFalse(destination.exists(), "Unsafe input must fail in preflight")
        self.assertEqual(sorted(p.name for p in self.base.iterdir()), ["tiny.zip"])

    def test_verify_accepts_exact_pinned_tiny_zip(self):
        path = self.archive([("folder/proof.txt", b"not a mathematical proof\n")])
        helper.verify(path, self.entry(path))
        self.assertEqual(helper.sha256(path), self.entry(path)["sha256"])

    def test_verify_rejects_wrong_size(self):
        path = self.archive([("file.txt", b"small")])
        with self.assertRaises(ValueError):
            helper.verify(path, self.entry(path, bytes=path.stat().st_size + 1))

    def test_verify_rejects_wrong_hash(self):
        path = self.archive([("file.txt", b"small")])
        with self.assertRaises(ValueError):
            helper.verify(path, self.entry(path, sha256="0" * 64))

    def test_verify_rejects_empty_archive(self):
        path = self.archive([])
        with self.assertRaises(ValueError):
            helper.verify(path, self.entry(path))

    def test_verify_rejects_nonzip_even_with_matching_pin(self):
        path = self.base / "not-a-zip.zip"
        path.write_bytes(b"not a ZIP archive")
        with self.assertRaises(zipfile.BadZipFile):
            helper.verify(path, self.entry(path))

    def test_existing_verified_download_does_not_use_network(self):
        path = self.archive([("file.txt", b"small")])
        with contextlib.redirect_stdout(io.StringIO()):
            helper.download(self.manifest(), self.entry(path), self.base)
        helper.urllib.request.urlopen.assert_not_called()

    def test_existing_bad_download_is_not_overwritten(self):
        path = self.archive([("file.txt", b"small")])
        old = path.read_bytes()
        with self.assertRaises(ValueError):
            helper.download(self.manifest(), self.entry(path, sha256="0" * 64), self.base)
        self.assertEqual(path.read_bytes(), old)
        helper.urllib.request.urlopen.assert_not_called()

    def test_download_rejects_manifest_directory_traversal(self):
        with self.assertRaises(ValueError):
            helper.download(
                self.manifest(),
                {"name": "../escape.zip", "bytes": 0, "sha256": "0" * 64},
                self.base,
            )
        helper.urllib.request.urlopen.assert_not_called()
        self.assertEqual(list(self.base.iterdir()), [])

    def test_existing_partial_download_is_not_overwritten(self):
        partial = self.base / "tiny.zip.part"
        partial.write_bytes(b"retain interrupted download")
        with self.assertRaises(FileExistsError):
            helper.download(
                self.manifest(),
                {"name": "tiny.zip", "bytes": 0, "sha256": "0" * 64},
                self.base,
            )
        self.assertEqual(partial.read_bytes(), b"retain interrupted download")
        helper.urllib.request.urlopen.assert_not_called()

    def test_mocked_download_checks_pin_before_promotion(self):
        source = self.archive([("file.txt", b"offline tiny payload")], "source.zip")
        payload = source.read_bytes()
        entry = self.entry(source, name="downloaded.zip")
        with mock.patch.object(helper.urllib.request, "urlopen", return_value=io.BytesIO(payload)) as opened:
            with contextlib.redirect_stdout(io.StringIO()):
                helper.download(self.manifest(), entry, self.base)
        opened.assert_called_once()
        request = opened.call_args.args[0]
        self.assertEqual(request.full_url, "https://github.com/example/project/releases/download/unit-test/downloaded.zip")
        self.assertEqual(opened.call_args.kwargs["timeout"], 90)
        self.assertEqual((self.base / "downloaded.zip").read_bytes(), payload)
        self.assertFalse((self.base / "downloaded.zip.part").exists())

    def test_oversize_mocked_download_is_not_promoted(self):
        entry = {"name": "downloaded.zip", "bytes": 1, "sha256": "0" * 64}
        with mock.patch.object(helper.urllib.request, "urlopen", return_value=io.BytesIO(b"too long")):
            with self.assertRaises(ValueError):
                helper.download(self.manifest(), entry, self.base)
        self.assertFalse((self.base / "downloaded.zip").exists())
        self.assertTrue((self.base / "downloaded.zip.part").exists())

    def test_wrong_hash_mocked_download_is_not_promoted(self):
        source = self.archive([("file.txt", b"small")], "source.zip")
        payload = source.read_bytes()
        entry = self.entry(source, name="downloaded.zip", sha256="0" * 64)
        with mock.patch.object(helper.urllib.request, "urlopen", return_value=io.BytesIO(payload)):
            with self.assertRaises(ValueError):
                helper.download(self.manifest(), entry, self.base)
        self.assertFalse((self.base / "downloaded.zip").exists())

    def test_promotion_never_overwrites_concurrently_created_target(self):
        source = self.archive([("file.txt", b"small")], "source.zip")
        payload = source.read_bytes()
        target = self.base / "downloaded.zip"

        def response_creating_target(*args, **kwargs):
            target.write_bytes(b"another process created this")
            return io.BytesIO(payload)

        with mock.patch.object(helper.urllib.request, "urlopen", side_effect=response_creating_target):
            with self.assertRaises(FileExistsError):
                helper.download(self.manifest(), self.entry(source, name=target.name), self.base)
        self.assertEqual(target.read_bytes(), b"another process created this")
        self.assertTrue((self.base / "downloaded.zip.part").exists())

    def test_extracts_nested_unicode_files_and_skips_finder_noise(self):
        path = self.archive([
            ("epoch/", b""),
            ("epoch/za\u017c\u00f3\u0142\u0107.txt", b"tiny source bytes\n"),
            ("__MACOSX/epoch/._file", b"finder metadata"),
            ("epoch/._file", b"finder metadata"),
        ])
        destination = self.base / "isolated"
        helper.extract_isolated(path, destination)
        self.assertEqual((destination / "epoch" / "za\u017c\u00f3\u0142\u0107.txt").read_bytes(), b"tiny source bytes\n")
        self.assertFalse((destination / "__MACOSX").exists())
        self.assertFalse((destination / "epoch" / "._file").exists())

    def test_extract_refuses_existing_destination(self):
        path = self.archive([("file.txt", b"small")])
        destination = self.base / "existing"
        destination.mkdir()
        sentinel = destination / "keep.txt"
        sentinel.write_bytes(b"keep")
        with self.assertRaises(FileExistsError):
            helper.extract_isolated(path, destination)
        self.assertEqual(sentinel.read_bytes(), b"keep")

    def test_rejects_traversal_absolute_and_ads(self):
        for name in ("../escape", "safe/../../escape", "/absolute", "C:/drive", "dir/file:ads"):
            with self.subTest(name=name):
                self.rejected_extraction([(name, b"tiny")])

    def test_rejects_raw_backslash_metadata(self):
        # ZipInfo itself normalizes backslashes on Windows. Set the raw
        # metadata after construction so this preflight test is OS-independent.
        info = zipfile.ZipInfo("placeholder")
        info.filename = "dir\\file"
        info.orig_filename = info.filename
        archive = mock.MagicMock()
        archive.__enter__.return_value = archive
        archive.infolist.return_value = [info]
        destination = self.base / "new-output"
        with mock.patch.object(helper.zipfile, "ZipFile", return_value=archive):
            with self.assertRaises(ValueError):
                helper.extract_isolated(self.base / "metadata-only.zip", destination)
        archive.open.assert_not_called()
        self.assertFalse(destination.exists())

    def test_rejects_full_path_case_collision(self):
        self.rejected_extraction([("file.txt", b"one"), ("FILE.TXT", b"two")])

    def test_rejects_directory_prefix_case_collision(self):
        self.rejected_extraction([("Epoch/one.txt", b"one"), ("epoch/two.txt", b"two")])

    def test_rejects_windows_reserved_components(self):
        for name in ("CON", "dir/NUL.txt", "COM1.py", "dir/LPT9", "aux/data.txt",
                     "COM\u00b9.txt", "dir/LPT\u00b2.py", "COM\u00b3"):
            with self.subTest(name=name):
                self.rejected_extraction([(name, b"tiny")])

    def test_rejects_windows_invalid_punctuation(self):
        for char in '<>:"|?*':
            with self.subTest(char=char):
                self.rejected_extraction([("dir/file" + char + "name", b"tiny")])

    def test_rejects_trailing_dot_or_space_components(self):
        for name in ("file.", "file ", "dir./file", "dir /file"):
            with self.subTest(name=name):
                self.rejected_extraction([(name, b"tiny")])

    def test_rejects_control_characters(self):
        for name in ("file\nname", "dir/\x01file", "dir\t/file"):
            with self.subTest(name=name):
                self.rejected_extraction([(name, b"tiny")])

    def test_rejects_file_used_as_directory_in_either_order(self):
        for entries in (
            [("ancestor", b"file"), ("ancestor/child", b"child")],
            [("ancestor/child", b"child"), ("ancestor", b"file")],
        ):
            with self.subTest(entries=entries):
                self.rejected_extraction(entries)

    def test_insufficient_disk_space_fails_before_creation(self):
        path = self.archive([("file.txt", b"small")])
        destination = self.base / "new-output"
        with mock.patch.object(helper.shutil, "disk_usage", return_value=mock.Mock(free=0)):
            with self.assertRaises(OSError):
                helper.extract_isolated(path, destination)
        self.assertFalse(destination.exists())

    def test_rejects_symbolic_links(self):
        link = zipfile.ZipInfo("link")
        link.create_system = 3
        link.external_attr = 0o120777 << 16
        self.rejected_extraction([(link, b"../outside")])

    def test_extraction_budget_is_checked_without_large_allocation(self):
        info = zipfile.ZipInfo("oversize.txt")
        info.file_size = 16 * 1024**3 + 1
        archive = mock.MagicMock()
        archive.__enter__.return_value = archive
        archive.infolist.return_value = [info]
        destination = self.base / "new-output"
        with mock.patch.object(helper.zipfile, "ZipFile", return_value=archive):
            with self.assertRaises(ValueError):
                helper.extract_isolated(self.base / "metadata-only.zip", destination)
        archive.open.assert_not_called()
        self.assertFalse(destination.exists())

    def test_crc_failure_does_not_report_success(self):
        path = self.archive([("payload.txt", b"stored payload")])
        with zipfile.ZipFile(path) as archive:
            info = archive.getinfo("payload.txt")
        data = bytearray(path.read_bytes())
        offset = info.header_offset + 30 + len(info.filename.encode("utf-8")) + len(info.extra)
        data[offset] ^= 1
        path.write_bytes(data)
        with self.assertRaises(zipfile.BadZipFile):
            helper.extract_isolated(path, self.base / "partial-output")
        self.assertFalse((self.base / "payload.txt").exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
