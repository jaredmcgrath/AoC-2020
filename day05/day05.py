#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advent of Code 2020
Day 5

Created on 2021-11-22T21:40:58.289324

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
        from ..helpers import get_input_lines
    else:
        from helpers import get_input_lines

    data = get_input_lines()

    return data

# %% Part 1


def part1(data):
    import math

    ids = []
    maxID = -1
    for line in data:
        rowLow = 0
        rowHigh = 127
        for c in line[:7]:
            if (c == "F"):
                rowHigh = math.floor((rowHigh + rowLow) / 2)
            else:
                rowLow = math.ceil((rowHigh + rowLow) / 2)
        row = rowLow
        seatLow = 0
        seatHigh = 7
        for c in line[7:10]:
            if (c == "L"):
                seatHigh = math.floor((seatHigh + seatLow) / 2)
            else:
                seatLow = math.ceil((seatHigh + seatLow) / 2)
        seat = seatLow
        seatID = row * 8 + seat
        ids.append(seatID)
        if (seatID > maxID):
            maxID = seatID
    return maxID, ids

# %% Part 2


def part2(ids):
    prevInIDs = False
    for i in range(1, 1023):
        if i in ids:
            prevInIDs = True
        elif i not in ids and prevInIDs:
            return i


# %% Run all
if __name__ == "__main__":
    data = load_data()
    result1, ids = part1(data)

    print(result1)
    print(part2(ids))

# %%
