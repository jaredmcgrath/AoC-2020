#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Initialize a new day for the AoC challenge.

Copies the default template in `default/`, setting the name, config, etc.
properly.

Created on Sat Nov 20 2021

@author: jaredmcgrath
"""

import os
import shutil
import re
import datetime


def get_author():
    """
    Uses the author set in AOC_AUTHOR env variable, or prompts stdin otherwise
    """
    author = os.environ.get("AOC_AUTHOR", None)
    if not author:
        author = input("Enter author name:\n")
    return author


def get_int_env(key, min, max, prompt):
    """
    Gets an int value from env variable, or prompts stdin otherwise
    """
    try:
        num = int(os.environ.get(key, None))
        if not (min <= num <= max):
            num = None
    except (TypeError, ValueError):
        num = None
    while not num:
        try:
            num = int(input("\n{}\n".format(prompt)))
            if not (min <= num <= max):
                print("Value must be {} - {}, inclusive".format(min, max))
                num = None
        except ValueError:
            print("Please enter an integer")
    return num


def get_timestamp():
    return datetime.datetime.now().isoformat()


def make_file_comment(day):
    year = get_int_env("AOC_YEAR", 2015, 2099, "Enter AoC year:")
    author = get_author()
    timestamp = get_timestamp()
    content = \
        '''"""
Advent of Code {}
Day {}

Created on {}

@author: {}
"""'''.format(year, day, timestamp, author)
    return content


def replace_template_comment(content, day):
    comment = make_file_comment(day)
    regex = "# START template_info(.|\\n)*# END template_info"
    split_content = re.split(regex, content)
    # Now join together first and last items in split_content with the new comment
    replaced_content = comment.join([split_content[0], split_content[-1]])
    return replaced_content


def set_solution_file(day, path="default.py"):
    """Sets the solution file to correct name and replaces content.
    Assumes it is in the directory with the default template solution script"""
    day_dirname = "day%02d" % day
    sol_filename = "{}.py".format(day_dirname)

    # Read existing file
    try:
        f = open(path)
        content = f.read()
        f.close()
        os.remove(path)
    except:
        raise IOError("Could not read default file content")

    # Open new file
    with open(sol_filename, "w") as f:
        replaced_content = replace_template_comment(content, day)
        f.write(replaced_content)


def copy_default(default_path="default/"):
    day = get_int_env("AOC_DAY", 1, 25, "Enter AoC day:")
    day_dirname = "day%02d" % day

    # Copy the default tree
    try:
        shutil.copytree(default_path, day_dirname)
    except FileExistsError:
        raise FileExistsError(
            "Day {} already exists!\n(path: {})".format(day, day_dirname))
    # Move to the new day
    try:
        os.chdir(day_dirname)
        set_solution_file(day)
        # Move back
        os.chdir("../")
    except OSError:
        print("could not ")


if __name__ == "__main__":
    copy_default()
