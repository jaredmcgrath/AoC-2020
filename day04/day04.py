#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advent of Code 2020
Day 4

Created on 2021-11-22T21:40:56.153736

@author: jaredmcgrath
"""
# %% Data loading


def find_path_to_helpers(target_folder="helpers", quiet=False):
    # Skip path finding if we successfully import the dummy file
    try:
        from helpers.dummy import dummy_func
        dummy_func()
        return
    except ImportError:
        not quiet and print("", "Couldn't find helpers directory!",
                            "Searching for path...", sep="\n")

    import os
    import sys
    # Figure out where this file is located so we can work backwards to find the target folder
    file_directory = os.path.dirname(os.path.abspath(__file__))
    path_check = []

    # Check parent directories to see if we hit the main project directory containing the target folder
    prev_working_path = working_path = file_directory
    while True:

        # If we find the target folder in the given directory, add it to the python path (if it's not already there)
        if target_folder in os.listdir(working_path):
            if working_path not in sys.path:
                tilde_swarm = "~"*(4 + len(working_path))
                not quiet and print("\n{}\nPython path updated:\n  {}\n{}".format(
                    tilde_swarm, working_path, tilde_swarm))
                sys.path.append(working_path)
            break

        # Stop if we hit the filesystem root directory (parent directory isn't changing)
        prev_working_path, working_path = working_path, os.path.dirname(
            working_path)
        path_check.append(prev_working_path)
        if prev_working_path == working_path:
            not quiet and print("\nTried paths:", *path_check, "", sep="\n  ")
            raise ImportError(
                "Can't find '{}' directory!".format(target_folder))


def load_data(quiet=True):
    find_path_to_helpers(quiet=quiet)
    if __package__:
        from ..helpers import get_input
    else:
        from helpers import get_input

    data = get_input().split("\n\n")

    return data

# %% Part 1


def part1(data):
    keys = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid", "cid"]
    valid = 0
    proper = []
    for passport in data:
        ppDict = {}
        entries = []
        for line in passport.split("\n"):
            for item in line.split(" "):
                (key, val) = item.split(":")
                entries.append(key)
                ppDict[key] = val
        missing = [x for x in filter(lambda x: not x in entries, keys)]
        if len(missing) == 0:
            valid += 1
            proper.append(ppDict)
        elif len(missing) == 1 and missing[0] == "cid":
            valid += 1
            proper.append(ppDict)
    return valid, proper

# %% Part 2


def part2(data):
    import re

    valid = 0
    for pp in proper:
        if (not 1920 <= int(pp["byr"]) <= 2002):
            continue
        if (not 2010 <= int(pp["iyr"]) <= 2020):
            continue
        if (not 2020 <= int(pp["eyr"]) <= 2030):
            continue
        if re.match('([0-9])+(cm|in)', pp["hgt"]):
            hgtUnit = pp["hgt"][len(pp["hgt"]) - 2:]
            hgtVal = int(pp["hgt"][:len(pp["hgt"]) - 2])
            if hgtUnit == "in" and not 59 <= hgtVal <= 76:
                continue
            elif hgtUnit == "cm" and not 150 <= hgtVal <= 193:
                continue
        else:
            continue
        if not re.match('#([0-9a-f]){6}', pp["hcl"]):
            continue
        validEcl = "amb blu brn gry grn hzl oth".split(" ")
        if not pp["ecl"] in validEcl:
            continue
        if len(pp["pid"]) != 9 or not pp["pid"].isnumeric():
            continue
        valid += 1
    return valid


# %% Run all
if __name__ == "__main__":
    data = load_data()
    result1, proper = part1(data)

    print(result1)
    print(part2(proper))

# %%
