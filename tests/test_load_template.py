from nose2.tools import params

from github_board import load_template

try:
    import unittest2 as unittest
except ImportError:
    import unittest

try:
    import mock
except ImportError:
    import unittest.mock as mock


class TestLoadTemplate(unittest.TestCase):
    @params(
        ("1", [[1]]),
        ("01", [[0, 1]]),
        ("0\n1", [[0], [1]]),
        ("1\n0\n", [[1], [0]]),
        ("10\n01", [[1, 0], [0, 1]]),
        ("\n1", [[1]]),
        ("", []),
        ("\n", []),

    )
    def test(self, content, expected_result):
        with mock.patch('github_board.open', mock.mock_open(read_data=content), create=True):
            self.assertListEqual(expected_result, load_template("fake_path"))
