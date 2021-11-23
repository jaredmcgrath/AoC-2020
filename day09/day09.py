#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advent of Code 2020
Day 9

Created on 2021-11-22T22:49:28.834154

@author: jaredmcgrath
"""
# %% Data loading


from typing import List
import itertools
from functools import reduce


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
        from ..helpers import get_input, ints
    else:
        from helpers import get_input, ints

    data = ints(get_input())

    return data


# %% Part 1


def checkSum(num: int, allNums: List[int]):
    for x, y in itertools.combinations(allNums, 2):
        if x+y == num:
            return True
    return False


def part1(data):
    WINDOW = 25
    for offset in range(WINDOW, len(data)):
        num = data[offset]
        prevNums = data[offset-WINDOW:offset]
        if not checkSum(num, prevNums):
            return num


# %% Part 2

# An efficient program
# to print subarray
# with sum as given sum

# Returns true if the
# there is a subarray
# of arr[] with sum
# equal to 'sum'
# otherwise returns
# false. Also, prints
# the result.
def subArraySum(arr: List[int], n, sum_):

    # Initialize curr_sum as
    # value of first element
    # and starting point as 0
    curr_sum = arr[0]
    start = 0

    # Add elements one by
    # one to curr_sum and
    # if the curr_sum exceeds
    # the sum, then remove
    # starting element
    i = 1
    while i <= n:

        # If curr_sum exceeds
        # the sum, then remove
        # the starting elements
        while curr_sum > sum_ and start < i-1:

            curr_sum = curr_sum - arr[start]
            start += 1

        # If curr_sum becomes
        # equal to sum, then
        # return true
        if curr_sum == sum_:
            return arr[start:i-1]

        # Add this element
        # to curr_sum
        if i < n:
            curr_sum = curr_sum + arr[i]
        i += 1

    return None


def part2(data, invalidNum):
    subArr = subArraySum(data, len(data), invalidNum)
    if subArr:
        min_ = reduce(min, subArr)
        max_ = reduce(max, subArr)
        return min_ + max_
    return -1


# %% Run all
if __name__ == "__main__":
    data = load_data()

    result1 = part1(data)

    print(result1)
    print(part2(data, result1))

# %%
