#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
 ░░░▒██░▒█░░░░▒█░▒█░░░░▒█░░░░░▒█░░░░░░░░░░░░░░░░▒█░░░
 ░░▒█░░░░░░▒█░▒█░▒█░░░░▒█░░░░░▒█░░░░░░░░░░░░░░░░▒█░░░
 ░░▒█▒██▒█▒███▒████▒█▒█▒███░░░▒███▒███▒███▒███▒███░░░
 ░░▒█░▒█▒█░▒█░▒█░▒█▒█▒█▒█▒█▒██▒█▒█▒█▒█▒███▒█░░▒█▒█░░░
 ░░░▒██░▒█░▒██▒█░▒█▒███▒███░░░▒███▒███▒█▒█▒█░░▒███░░░
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
"""

import argparse
import datetime
import time

import pygit2

STEP = 86400  # seconds in a day
UTC_TO_PST_OFFSET = 28800  # seconds in 8 hours
COMMIT_MULTIPLIER = 1


def board_origin(today):
    """
    Calculates point 0×0 (top left corner of the board) in seconds (in PST)

    :type today: datetime.date
    :rtype: int
    """
    last_cell_dt = today
    first_cell_dt = datetime.date(last_cell_dt.year - 1, last_cell_dt.month, last_cell_dt.day)
    first_cell_ux = time.mktime(first_cell_dt.timetuple()) - time.timezone + UTC_TO_PST_OFFSET  # localtime → PST
    return int(first_cell_ux) + sunday_offset(first_cell_dt)


def sunday_offset(date):
    """
    Calculates time from date to the next sunday in seconds

    :type date: datetime.date
    :rtype: int
    """
    return (7 - (datetime.date.weekday(date) + 1) % 7) * STEP


def template_to_tape(template, origin):
    """
    Converts template to tape of timestamps

    :type template: list of list of int
    :type origin: int
    :rtype: list of int
    """
    tape = []
    (i, j) = (0, 0)
    for row in template:
        for col in row:
            if col > 0:
                tape.extend([origin + (i * 7 + j) * STEP] * col)
            i += 1
        i, j = 0, j + 1
    return tape


def load_template(file_path):
    """
    Loads template from file

    :type file_path: str
    :rtype: list of list of int
    """
    template = []
    f = open(file_path, "r")
    l = []
    for c in f.read():
        if c.isdigit():
            l.append(int(c) * COMMIT_MULTIPLIER)
        elif c == "\n" and l:
            template.append(l)
            l = []
    if l:
        template.append(l)
    f.close()
    return template


def main(*args):
    """
    The main program

    :type args: tuple
    """
    email, repo_path, tpl_file = args
    tpl = load_template(tpl_file)

    try:
        repo = pygit2.Repository(repo_path)
    except KeyError:
        raise Exception("'{path}' - not a git repository".format(path=repo_path))

    if email is None:
        emails = repo.config.get_multivar("user.email")
        emails = []
        if len(emails) > 0:
            email = emails[~0]
        else:
            raise Exception("You should specify email by command line parameter (--email or -e) "
                            "or use one of the configuration files of the git")

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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GitHub board — …")
    parser.add_argument("-r", "--repo", required=True, help="path to your git repository")
    parser.add_argument("-e", "--email", help="your GitHub email, if not set, email from git config will be used")
    parser.add_argument("-t", "--template", required=True, help="path to file with template")
    arguments = parser.parse_args()
    main(arguments.email, arguments.repo, arguments.template)
