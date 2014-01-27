from nose2.tools import params

from test import mock
from test import RepoTestCase

from github_board import main


class TestMain(RepoTestCase):
    @params(
        ("0",),
        ("1\n",),
        ("4",),
        ("123\n405670\n80",),
    )
    def test(self, template):
        with mock.patch("github_board.open", mock.mock_open(read_data=template), create=True):
            with mock.patch("github_board.pygit2.Repository.create_commit", mock.Mock()) as m:
                main("test@test", self.repo_path, template, None)
                self.assertEquals(sum([int(i) for i in template if i.isdigit()]), len(m.mock_calls))
