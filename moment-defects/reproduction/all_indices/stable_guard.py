"""Race-tolerant private-output inventory, without weakening resource guards.

The native writer exclusively creates a file and atomically publishes it by
rename. A directory enumeration can therefore contain a name which vanishes
before its stat. Such an enumeration is discarded in full, never partially
accepted. Two consecutive complete inventories must agree. This preserves the
original guard's sampled quota semantics; it is not a filesystem transaction
or a guarantee against an arbitrary adversarial concurrent writer.
"""
from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path
import shutil
import stat


class StableScanError(RuntimeError):
    """No complete, stable, safe private-output inventory was obtained."""


class _ChangedDuringScan(Exception):
    """Discard the entire current inventory and restart at its root."""


@dataclass(frozen=True)
class Inventory:
    entries: tuple
    total_bytes: int


def _need(condition, message):
    if not condition:
        raise StableScanError(message)


def _identity(value):
    return (value.st_dev, value.st_ino, stat.S_IFMT(value.st_mode),
            value.st_size, value.st_mtime_ns,
            getattr(value, "st_file_attributes", 0))


def _safe_stat(value):
    attributes = getattr(value, "st_file_attributes", 0)
    reparse = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
    _need(not stat.S_ISLNK(value.st_mode) and not (attributes & reparse),
          "No private-scratch symlink or reparse point")
    _need(stat.S_ISDIR(value.st_mode) or stat.S_ISREG(value.st_mode),
          "Only regular files and directories in private scratch")


def _same(left, right):
    if _identity(left) != _identity(right):
        raise _ChangedDuringScan("Private output identity or size changed")


def _contained(path, root):
    resolved = path.resolve(strict=True)
    _need(resolved == root or resolved.is_relative_to(root),
          "Private output remains within its resolved private root")


def _file_stat(path, expected, root):
    """Sample a regular file through a descriptor and revalidate its name."""
    _safe_stat(expected)
    _need(stat.S_ISREG(expected.st_mode), "Private output file is regular")
    _contained(path, root)
    flags = os.O_RDONLY | getattr(os, "O_BINARY", 0) | getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(path, flags)
    try:
        opened = os.fstat(descriptor)
        _safe_stat(opened)
        _need(stat.S_ISREG(opened.st_mode), "Opened private output is regular")
        _same(expected, opened)
        _same(opened, os.fstat(descriptor))
        named = path.lstat()
        _safe_stat(named)
        _same(opened, named)
        _contained(path, root)
        return opened
    finally:
        os.close(descriptor)


def _scan_once(work, byte_limit):
    """Return one full inventory or discard it on an observed concurrent change."""
    work = Path(work)
    initial = work.lstat()
    _safe_stat(initial)
    _need(stat.S_ISDIR(initial.st_mode), "Private scratch root is a directory")
    root = work.resolve(strict=True)
    entries = []
    used = 0

    def visit(directory, expected):
        nonlocal used
        current = directory.lstat()
        _safe_stat(current)
        _need(stat.S_ISDIR(current.st_mode), "Private scratch directory is regular")
        _same(expected, current)
        _contained(directory, root)
        relative = directory.relative_to(work).as_posix()
        entries.append((relative, "directory", *_identity(current)))
        with os.scandir(directory) as iterator:
            children = sorted(iterator, key=lambda item: item.name)
        for child in children:
            path = directory / child.name
            value = path.lstat()
            _safe_stat(value)
            if stat.S_ISDIR(value.st_mode):
                visit(path, value)
            else:
                value = _file_stat(path, value, root)
                used += value.st_size
                _need(used <= byte_limit,
                      "All private source/output/checkpoint files exceed256MiB quota")
                entries.append((path.relative_to(work).as_posix(), "file", *_identity(value)))
        after = directory.lstat()
        _safe_stat(after)
        _same(current, after)
        _contained(directory, root)

    try:
        visit(work, initial)
        _same(initial, work.lstat())
    except FileNotFoundError as exc:
        raise _ChangedDuringScan("A listed private output vanished; discard full scan") from exc
    return Inventory(tuple(entries), used)


def stable_inventory(work, byte_limit, max_scans=8):
    """Require two identical complete scans; instability always fails closed."""
    _need(type(byte_limit) is int and byte_limit >= 0, "Literal nonnegative byte quota")
    _need(type(max_scans) is int and max_scans >= 2, "At least two bounded scans")
    previous = None
    for _ in range(max_scans):
        try:
            current = _scan_once(work, byte_limit)
        except _ChangedDuringScan:
            previous = None
            continue
        if previous == current:
            return current
        previous = current
    raise StableScanError("No two identical complete private-output inventories; no acceptance")


def install(runner):
    """Install only the output-scan replacement; keep original RAM/CPU guards."""
    _need(not getattr(runner, "_stable_private_guard_installed", False),
          "Stable private-output guard installed once")
    original = runner.parent_guard

    def parent_guard(tiny=False, work=None):
        # Original sampled peak-RSS, host-reserve and tiny CPU checks remain.
        original(tiny=tiny)
        if work is not None:
            runner.require(shutil.disk_usage(work).free >= runner.DISK_FLOOR,
                           "Private scratch disk floor4GiB")
            stable_inventory(work, runner.WORK_LIMIT)
            # A lengthy/unstable scan must not evade the resource checks.
            original(tiny=tiny)

    runner.parent_guard = parent_guard
    runner._stable_private_guard_installed = True
