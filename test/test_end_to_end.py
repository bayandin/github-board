import subprocess

from nose2.tools import params

from test import RepoTestCase


class TestEndToEnd(RepoTestCase):
    @params(
        ("",),
        ("center",),
    )
    def test(self, alignment):
        return_code = subprocess.call([
            "./github_board.py",
            "-r", self.repo.path,
            "-t", "./templates/default.tpl",
            "-e", "test@test",
            "-a", alignment,
        ])
        self.assertEqual(0, return_code)
