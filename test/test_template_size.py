from nose2.tools import params

from test import unittest

from github_board import template_size


class TestTemplateSize(unittest.TestCase):
    @params(
        ([], {"height": 0, "width": 0}),
        ([[1]], {"height": 1, "width": 1}),
        ([[1, 2]], {"height": 1, "width": 2}),
        ([[1], [2]], {"height": 2, "width": 1}),
        ([[1, 2], [3, 4, 7], [6, 7], [8]], {"height": 4, "width": 3}),
    )
    def test(self, template, expected_result):
        self.assertDictEqual(expected_result, template_size(template))
