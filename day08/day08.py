#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advent of Code 2020
Day 8

Created on 2021-11-22T21:41:05.842651

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
    a = 0
    insP = 0
    run = []

    while True:
        if insP in run:
            return a
        ins = data[insP]
        run.append(insP)
        parts = ins.split(" ")
        op = parts[0]

        if op == "acc":
            a += int(parts[1])
            insP += 1
        elif op == "nop":
            insP += 1
        elif op == "jmp":
            insP += int(parts[1])

# %% Part 2


def part2(data):
    allChangeable = list(filter(lambda x: x[1].startswith(
        "nop") or x[1].startswith("jmp"), enumerate(data)))
    iChange = 0

    for iChange in range(-1, len(allChangeable)):
        # clone data
        nData = data.copy()
        # Make change
        if iChange >= 0:
            test = allChangeable[iChange]
            if test[1].startswith("jmp"):
                nData[test[0]] = " ".join(["nop", test[1].split(" ")[1]])
            else:
                nData[test[0]] = " ".join(["jmp", test[1].split(" ")[1]])
        # set state
        a = 0
        insP = 0
        run = []
        while insP < len(nData):
            if insP in run:
                break
            ins = nData[insP]
            run.append(insP)
            parts = ins.split(" ")
            op = parts[0]

            if op == "acc":
                a += int(parts[1])
                insP += 1
            elif op == "nop":
                insP += 1
            elif op == "jmp":
                insP += int(parts[1])
        if insP >= len(nData):
            return a


# %% Run all
if __name__ == "__main__":
    data = load_data()

    print(part1(data))
    print(part2(data))

# %%
