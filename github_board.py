#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
"""
 ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
 ░████░███░███░█░░█░█░░█░███░░███░░███░███░███░░███░░
 ░█░░░░░█░░░█░░█░░█░█░░█░█░█░░█░█░░█░█░█░█░█░█░░█░░█░
 ░█░██░░█░░░█░░████░█░░█░████░████░█░█░███░████░█░░█░
 ░█░░█░░█░░░█░░█░░█░█░░█░█░░█░█░░█░█░█░█░█░█░░█░█░░█░
 ░████░███░░█░░█░░█░████░████░████░███░█░█░█░░█░███░░
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
"""

import argparse
import datetime
import time

import pygit2

STEP = 86400  # seconds in a day
UTC_TO_PST_OFFSET = 28800  # seconds in 8 hours


def board_origin(today):
    """
    :type today: datetime.date
    :rtype: int
    """

    def offset(date):
        """
        :type date: datetime.date
        :rtype: int
        """
        return 14 - (datetime.date.weekday(date) + 1) % 7

    last_cell_dt = today
    first_cell_dt = datetime.date(last_cell_dt.year - 1, last_cell_dt.month, last_cell_dt.day)
    first_cell_ux = time.mktime(first_cell_dt.timetuple()) - time.timezone + UTC_TO_PST_OFFSET  # localtime → PST
    first_week_offset = offset(first_cell_dt) * STEP
    return int(first_cell_ux) + first_week_offset


def template_to_tape(template, origin):
    """
    :type template: list of list of int
    :type origin: int
    :rtype: list of int
    """
    tape = []
    (i, j) = (0, 0)
    for row in template:
        for col in row:
            if col == 1:
                tape.append(origin + (i * 7 + j) * STEP)
            i += 1
        i, j = 0, j + 1
    return tape


def load_template(filepath):
    """
    :type filepath: str
    :rtype: list of list of int
    """
    template = []
    f = file(filepath, "r")
    for l in f.readlines():
        template.append(map(int, list(l.strip())))
    f.close()
    return template


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Github Board — …")
    parser.add_argument("-p", "--path", required=True, help="path to git repository")
    parser.add_argument("-e", "--email", required=True, help="your github email")
    parser.add_argument("-t", "--template", required=True, help="path to file with template")
    args = parser.parse_args()
    email, path, tpl_file = args.email, args.path, args.template
    tpl = load_template(tpl_file)

    try:
        repo = pygit2.Repository(path)
    except KeyError:
        raise Exception("{path} - not a git repository".format(path=path))
    tree = repo.TreeBuilder().write()

    head_hex = [] if repo.is_empty else [repo.head.target.hex]
    for timestamp in template_to_tape(tpl, board_origin(datetime.date.today())):
        author = pygit2.Signature(name="Anonymous", email=email, time=timestamp)
        commit = repo.create_commit(
            "refs/heads/master",
            author,
            author,
            "",
            tree,
            head_hex
        )
        head_hex = [commit.hex]
