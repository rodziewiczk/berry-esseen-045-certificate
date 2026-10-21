"""Control-plane regression tests; these are not certificate acceptances."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import types
import unittest

from . import c5_gapfree, c5_inputs, supervised, windows_toolchain


class ReproducerTests(unittest.TestCase):
    def test_source_path_escape(self):
        for path in ('../bad', '/absolute', 'C:/bad', 'a//b', 'a/./b', 'a\\b'):
            with self.subTest(path=path), self.assertRaises(ValueError):
                c5_inputs.safe_relative(path)
        self.assertEqual(c5_inputs.safe_relative('work/a/file.py'), ('work', 'a', 'file.py'))

    def test_failure_preserves_diagnostics_and_exception(self):
        runner = types.SimpleNamespace(__file__=__file__)
        def run_child(*args, **kwargs):
            outputs = {'stdout': b'progress', 'stderr': b'precise failure'}
            process = types.SimpleNamespace(returncode=7)
            cpu = 1.25
            raise RuntimeError('original rejection')
        runner.run_child = run_child
        with tempfile.TemporaryDirectory() as directory:
            work = Path(directory)
            with self.assertRaisesRegex(RuntimeError, 'original rejection'):
                supervised.run_recorded(runner, [], work, 'test', 10, 1024)
            self.assertEqual((work/'test.failed.stderr.txt').read_bytes(), b'precise failure')
            packet = json.loads((work/'test.failure.json').read_text())
            self.assertEqual(packet['child_returncode'], 7)
            self.assertFalse(packet['arithmetic_accepted'])

    def test_cache_only_missing_files_does_not_download_or_create_destination(self):
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory)/'must-not-exist'
            old = sys.argv
            sys.argv = ['setup', '--directory', str(destination), '--cache', directory,
                        '--verify-cache-only']
            try:
                with self.assertRaises(ValueError):
                    windows_toolchain.main()
            finally:
                sys.argv = old
            self.assertFalse(destination.exists())

    def test_all_fails_closed(self):
        root = Path(__file__).resolve().parents[2]
        result = subprocess.run([sys.executable, '-B', '-S', str(root/'reproduce.py'), '--all'],
                                capture_output=True, text=True, timeout=20)
        self.assertEqual(result.returncode, 2)
        packet = json.loads(result.stdout)
        self.assertFalse(packet['all_computational_obligations_verified'])
        self.assertTrue(packet['missing_adapters'])


if __name__ == '__main__':
    unittest.main()
