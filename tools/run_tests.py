#!/usr/bin/env python3
"""Execute all tests; fail if missing timezone data causes any tests to skip."""
from __future__ import annotations
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    # Do not depend on the working directory or shell-specific PYTHONPATH settings.
    sys.path.insert(0, str(ROOT))
    suite = unittest.defaultTestLoader.discover(str(ROOT / 'tests'), pattern='test_*.py')
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if result.testsRun == 0:
        print('ERROR: test discovery found no tests', file=sys.stderr)
        return 1
    if result.skipped:
        print(f'ERROR: {len(result.skipped)} skipped test(s); all tests must execute', file=sys.stderr)
        return 1
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    raise SystemExit(main())
