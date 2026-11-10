#!/usr/bin/env python3
#
# This file is part of the aMule Project.
#
# Copyright (c) 2026 aMule Team ( https://amule-org.github.io )
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301, USA.
#

"""Exercise the smoke entry point up to browser preflight, without launching it."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(os.environ['AMULE_SOURCE_DIR']).resolve()


class PreflightTest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='ed2k-preflight-')
        self.addCleanup(self.temporary.cleanup)
        self.work = Path(self.temporary.name)
        self.source = self.work / 'source with spaces'
        # Use the real maintained helpers, including the lazy authentication
        # dependency chain and its protocol constants, rather than stub imports.
        shutil.copytree(SOURCE / 'unittests/tests', self.source / 'unittests/tests')
        codes = self.source / 'src/libs/ec/abstracts'
        codes.mkdir(parents=True)
        shutil.copyfile(SOURCE / 'src/libs/ec/abstracts/ECCodes.abstract', codes / 'ECCodes.abstract')
        self.bin = self.work / 'bin with spaces'
        self.bin.mkdir()
        self.binary = self.bin / 'amuled'
        self.binary.write_text('#!/bin/sh\nexit 99\n')
        self.binary.chmod(0o755)
        self.probe = self.work / 'browser-preflight.json'
        # This replaces only the browser executable probe. No browser, X server
        # or daemon may start; successful application preflight reaches here.
        node = self.bin / 'node'
        node.write_text('#!/usr/bin/env python3\nimport json, os\n'
                        'from pathlib import Path\n'
                        'Path(os.environ["PREFLIGHT_PROBE"]).write_text(json.dumps({key: os.environ.get(key) for key in ("AMULE_BINARY", "AMULE_SOURCE_DIR")}))\n'
                        'raise SystemExit(1)\n')
        node.chmod(0o755)
        self.env = dict(os.environ, PATH=str(self.bin) + os.pathsep + os.environ['PATH'],
                        PREFLIGHT_PROBE=str(self.probe), AMULE_BINARY=str(self.binary),
                        AMULE_SOURCE_DIR=str(self.source), PYTHONDONTWRITEBYTECODE='1')
        self.env.pop('PYTHONPATH', None)

    def run_preflight(self, reached_browser):
        result = subprocess.run(['bash', str(ROOT / 'tests/smoke.sh')],
                                cwd=self.work, env=self.env, capture_output=True,
                                text=True, timeout=20)
        self.assertEqual(result.returncode, 77, result.stdout + result.stderr)
        self.assertNotIn('Smoke evidence:', result.stdout)
        self.assertEqual(self.probe.exists(), reached_browser, result.stdout + result.stderr)
        return json.loads(self.probe.read_text()) if reached_browser else result.stderr

    def test_absolute_binary_and_source(self):
        env = self.run_preflight(True)
        self.assertEqual(env['AMULE_BINARY'], str(self.binary))
        self.assertEqual(env['AMULE_SOURCE_DIR'], str(self.source))

    def test_relative_binary_and_source_survive_cwd_change(self):
        self.env['AMULE_BINARY'] = './bin with spaces/amuled'
        self.env['AMULE_SOURCE_DIR'] = './source with spaces'
        env = self.run_preflight(True)
        self.assertEqual(env['AMULE_BINARY'], str(self.binary))
        self.assertEqual(env['AMULE_SOURCE_DIR'], str(self.source))
        # A desktop launcher is free to use a different working directory.
        result = subprocess.run([env['AMULE_BINARY']], cwd='/', check=False)
        self.assertEqual(result.returncode, 99)

    def test_binary_on_relative_search_path(self):
        self.env['PATH'] = 'bin with spaces' + os.pathsep + os.environ['PATH']
        self.env['AMULE_BINARY'] = 'amuled'
        env = self.run_preflight(True)
        self.assertEqual(env['AMULE_BINARY'], str(self.binary))

    def test_logging_only_needs_no_source(self):
        self.env.pop('AMULE_BINARY')
        self.env.pop('AMULE_SOURCE_DIR')
        self.run_preflight(True)

    def test_missing_source(self):
        self.env.pop('AMULE_SOURCE_DIR')
        self.assertIn('AMULE_SOURCE_DIR', self.run_preflight(False))

    def test_nonexistent_source(self):
        self.env['AMULE_SOURCE_DIR'] = str(self.work / 'absent')
        self.run_preflight(False)

    def test_nonexecutable_binary(self):
        self.binary.chmod(0o644)
        self.run_preflight(False)

    def test_missing_helpers_fail_before_browser(self):
        for name in ['DaemonConfig.py', 'AllSearchIntegrationTest.py', 'ECWire.py', 'ECSRPVector.py']:
            with self.subTest(helper=name):
                helper = self.source / 'unittests/tests' / name
                content = helper.read_bytes()
                helper.unlink()
                try:
                    self.run_preflight(False)
                finally:
                    helper.write_bytes(content)
                    self.probe.unlink(missing_ok=True)


if __name__ == '__main__':
    unittest.main()
