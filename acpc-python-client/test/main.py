import unittest
from unittest import TestSuite

from test.data_tests import (
    GameTest,
    StateTest,
    MatchStateTest
)
from test.wrappers_tests import (
    GameWrapperTest,
    ActionWrapperTest,
    PossibleActionsWrapperTest,
    MatchStateWrapperTest,
    StateWrapperTest
)
from test.game_utils_test import GameUtilsTest

test_classes = [
    ActionWrapperTest,
    GameWrapperTest,
    StateWrapperTest,
    MatchStateWrapperTest,
    PossibleActionsWrapperTest,
    GameTest,
    StateTest,
    MatchStateTest,
    GameUtilsTest
]


def load_tests(loader, tests, pattern):
    suite = TestSuite()
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    return suite


if __name__ == "__main__":
    unittest.main()
