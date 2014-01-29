import datetime

from nose2.tools import params

from test import GithubBoardTestCase

from github_board import STEP, sunday_offset


class TestSundayOffset(GithubBoardTestCase):
    @params(
        (datetime.date(2014, 1, 19), 7 * STEP),   # Sunday
        (datetime.date(2007, 12, 31), 6 * STEP),  # Monday
        (datetime.date(2038, 1, 19), 5 * STEP),   # Tuesday
        (datetime.date(2012, 2, 29), 4 * STEP),   # Wednesday
        (datetime.date(1970, 1, 1), 3 * STEP),    # Thursday
        (datetime.date(1990, 11, 30), 2 * STEP),  # Friday
        (datetime.date(2007, 7, 28), STEP),       # Saturday
    )
    def test(self, date, expected_result):
        self.assertEqual(expected_result, sunday_offset(date))
