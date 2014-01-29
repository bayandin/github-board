import datetime
import os
import time

from nose2.tools import params

from test import mock
from test import GithubBoardTestCase

from github_board import board_origin, UTC_TO_PST_OFFSET


class TestBoardOrigin(GithubBoardTestCase):
    @params(
        (datetime.date(1971, 1, 1), "UTC", 0, UTC_TO_PST_OFFSET),
        (datetime.date(1971, 1, 1), "Asia/Novosibirsk", 0, UTC_TO_PST_OFFSET),
        (datetime.date(1971, 1, 1), "America/New_York", 0, UTC_TO_PST_OFFSET),
        (datetime.date(1971, 1, 1), "PST8PDT", 0, UTC_TO_PST_OFFSET),
        (datetime.date(1971, 1, 1), "UTC", 42, 42 + UTC_TO_PST_OFFSET),
        (datetime.date(2014, 1, 22), "Europe/Moscow", 0, 1358812800 + UTC_TO_PST_OFFSET),
    )
    def test(self, date, timezone, sunday_offset, expected_result):
        self.set_timezone(timezone)
        with mock.patch("github_board.sunday_offset", mock.Mock(return_value=sunday_offset)):
            self.assertEqual(expected_result, board_origin(date))

    @staticmethod
    def set_timezone(timezone):
        """
        Sets timezone

        :type timezone: str
        """
        os.environ["TZ"] = timezone
        time.tzset()
