from nose2.tools import params

from test import BytesIO
from test import GithubBoardTestCase
from test import mock

from github_board import min_max_for_user


class TestMinMaxForUser(GithubBoardTestCase):
    @params(
        (b'[["2013/10/21",0]]', (0, 0)),
        (b'[["2013/10/21",0],["2013/10/21",1]]', (1, 1)),
        (b'[["2013/10/21",2],["2013/10/21",1],["2013/10/21",0]]', (1, 2)),
    )
    def test(self, data, expected_result):
        with mock.patch("github_board.url_request.urlopen", mock.Mock(return_value=BytesIO(data))):
            self.assertSequenceEqual(expected_result, min_max_for_user("some_github_user"))
