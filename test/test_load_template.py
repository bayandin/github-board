from nose2.tools import params

from test import mock
from test import GithubBoardTestCase

from github_board import COMMIT_MULTIPLIER, load_template


class TestLoadTemplate(GithubBoardTestCase):
    @params(
        ("1", [[1 * COMMIT_MULTIPLIER]]),
        ("01", [[0, 1 * COMMIT_MULTIPLIER]]),
        ("0\n1", [[0], [1 * COMMIT_MULTIPLIER]]),
        ("1\n0\n", [[1 * COMMIT_MULTIPLIER], [0]]),
        ("10\n01", [[1 * COMMIT_MULTIPLIER, 0], [0, 1 * COMMIT_MULTIPLIER]]),
        ("\n1", [[1 * COMMIT_MULTIPLIER]]),
        ("", []),
        ("\n", []),
        ("5", [[5 * COMMIT_MULTIPLIER]]),
        ("123", [[1 * COMMIT_MULTIPLIER, 2 * COMMIT_MULTIPLIER, 3 * COMMIT_MULTIPLIER]]),
        ("1\n2\n3", [[1 * COMMIT_MULTIPLIER], [2 * COMMIT_MULTIPLIER], [3 * COMMIT_MULTIPLIER]]),
        ("12\n3", [[1 * COMMIT_MULTIPLIER, 2 * COMMIT_MULTIPLIER], [3 * COMMIT_MULTIPLIER]]),
    )
    def test(self, content, expected_result):
        with mock.patch("github_board.open", mock.mock_open(read_data=content), create=True):
            self.assertListEqual(expected_result, load_template("fake_path"))
