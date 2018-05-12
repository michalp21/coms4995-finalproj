import sys
import unittest
from unittest import TestSuite


def suite(test_name):
    suite = unittest.TestSuite()
    suite.addTest(unittest.defaultTestLoader.loadTestsFromName(test_name))
    return suite


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage {test_name}")
        sys.exit(1)

    runner = unittest.TextTestRunner()
    runner.run(suite(sys.argv[1]))
