import shutil

import pygit2

try:
    import unittest2 as unittest
except ImportError:
    import unittest

try:
    import mock
except ImportError:
    import unittest.mock as mock


class GithubBoardTestCase(unittest.TestCase):
    pass


class RepoTestCase(GithubBoardTestCase):
    def setUp(self):
        self.repo_path = pygit2.init_repository("./test/repo").path

    def tearDown(self):
        shutil.rmtree(self.repo_path)
