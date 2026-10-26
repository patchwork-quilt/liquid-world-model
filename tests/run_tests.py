"""Run the whole suite and print a one-line summary."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

if __name__ == "__main__":
    suite = unittest.TestLoader().discover(
        str(Path(__file__).resolve().parent))
    result = unittest.TextTestRunner(verbosity=1).run(suite)
    total = result.testsRun
    bad = len(result.failures) + len(result.errors)
    print(f"TEST SUMMARY: {total - bad}/{total} PASS")
    sys.exit(1 if bad else 0)
