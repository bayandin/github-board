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

try:
    from StringIO import StringIO as BytesIO
except ImportError:
    from io import BytesIO


class GithubBoardTestCase(unittest.TestCase):
    pass


class RepoTestCase(GithubBoardTestCase):
    def setUp(self):
        self.repo = pygit2.init_repository("./test/repo")

    def tearDown(self):
        shutil.rmtree(self.repo.path)
