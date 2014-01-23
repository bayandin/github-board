import mock

from nose2.tools import params
from unittest2 import TestCase

from github_board import load_template


class TestLoadTemplate(TestCase):
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
