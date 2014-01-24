import subprocess

from test import RepoTestCase


class TestEndToEnd(RepoTestCase):
    def test(self):
        return_code = subprocess.call([
            "./github_board.py",
            "-r", self.repo_path,
            "-t", "./templates/default.tpl",
            "-e", "test@test",
        ])
        self.assertEqual(0, return_code)
