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


def sunday_offset(date, reverse=False):
    """
    Calculates time from date to the next sunday or previous saturday in seconds

    :type date: datetime.date
    :type reverse: bool
    :rtype: int
    """
    if not reverse:
        offset = (7 - (datetime.date.weekday(date) + 1) % 7) * STEP
    else:
        offset = -((datetime.date.weekday(date) + 2) % 7) * STEP
    return offset


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


def template_size(template):
    """
    Returns template width and height

    :type template: list of list of int
    :rtype: dict
    """
    size = {
        "width": max([len(row) for row in template]) if len(template) > 0 else 0,
        "height": len(template),
    }
    return size


def align_template(template, alignment=None):
    """
    Returns aligned template

    :type template: list of list of int
    :type alignment: str
    :rtype: list of list of int
    """
    size = template_size(template)
    board = {
        "width": 51,
        "height": 7,
    }
    out = template[:]

    if alignment == "center":
        offset = {
            "width": int((board["width"] - size["width"]) / 2),
            "height": int((board["height"] - size["height"]) / 2),
        }
        for i in out:
            i[0:0] = [0] * offset["width"]
        for i in range(offset["height"]):
            out.insert(0, [0])
        return out
    else:
        return out


def main(*args):
    """
    The main program

    :type args: tuple
    """
    email, repo_path, tpl_file, alignment = args

    tpl = load_template(tpl_file)
    tpl = align_template(tpl, alignment)

    try:
        repo = pygit2.Repository(repo_path)
    except KeyError:
        raise RuntimeError("'{path}' - not a git repository".format(path=repo_path))

    if email is None:
        if "user.email" in repo.config:
            email = repo.config["user.email"]
        else:
            raise RuntimeError("You should specify email by command line parameter (--email or -e) "
                               "or use one of the configuration files of the git")

    tree = repo.TreeBuilder().write()

    head = [] if repo.is_empty else [str(repo.head.target)]
    for timestamp in template_to_tape(tpl, board_origin(datetime.date.today())):
        author = pygit2.Signature(name="Anonymous", email=email, time=timestamp)
        commit = repo.create_commit(
            "refs/heads/master",
            author,
            author,
            "",
            tree,
            head
        )
        head = [str(commit)]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GitHub board — …")
    parser.add_argument("-r", "--repo", required=True, help="path to your git repository")
    parser.add_argument("-e", "--email", help="your GitHub email, if not set, email from git config will be used")
    parser.add_argument("-t", "--template", required=True, help="path to file with template")
    parser.add_argument("-a", "--alignment", help="template alignment, supported variants: center")
    arguments = parser.parse_args()
    main(arguments.email, arguments.repo, arguments.template, arguments.alignment)
