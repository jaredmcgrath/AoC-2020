#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advent of Code 2020
Day 7

Created on 2021-11-22T21:41:02.998399

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


def accumulateUniqueParents(allBags, searches, unique=[], searched=[]):
    # If we have no more to search, return unique parents
    if (len(searches) == 0):
        return unique
    # Item to search for
    toBeSearched = searches.pop()
    if not toBeSearched in unique:
        unique.append(toBeSearched)
    # print(toBeSearched)
    if not toBeSearched in searched:
        searched.append(toBeSearched)
        # find all parents containing this bag
        parents = []
        for test in allBags:
            childrenMatch = list(
                filter(lambda x: x["bag_name"] == toBeSearched, test["children"]))
            if (len(childrenMatch) > 0):
                parents.append(test)
        for parent in parents:
            if not parent["bag_name"] in unique:
                unique.append(parent["bag_name"])
            if not parent["bag_name"] in searched:
                searches.append(parent["bag_name"])
    return accumulateUniqueParents(allBags, searches, unique, searched)


def part1(data):
    bags = []
    golds = []
    for line in data:
        bag_name = " ".join(line.split(" ")[:2])
        after_contains = line.split("contain ")[1]
        children = []
        for bag in after_contains.split(", "):
            words = bag.split(" ")
            count = int(words[0]) if words[0].isnumeric() else 0
            child_type = " ".join(words[1:3])
            children.append({"bag_name": child_type, "count": count})
            if child_type == "shiny gold":
                golds.append(bag_name)
        bags.append({"bag_name": bag_name, "children": children})
    unique = accumulateUniqueParents(bags, golds)
    return len(unique)

# %% Part 2


def countChildren(allBags, children, count=0):
    if len(children) == 0:
        return count
    child = children.pop()
    cCount = child["count"]
    count += child["count"]
    # Find this bag in allBags
    bags = list(filter(lambda x: x["bag_name"] == child["bag_name"], allBags))
    if (len(bags) > 0):
        bChildren = bags[0]["children"]
        childr2 = []
        for kid in bChildren:
            kidClone = kid.copy()
            kidClone["count"] = kid["count"] * cCount
            children.append(kidClone)
            childr2.append(kidClone)
    return countChildren(allBags, children, count)


def part2(data):
    bags = []
    kids = []
    for line in data:
        bag_name = " ".join(line.split(" ")[:2])
        after_contains = line.split("contain ")[1]
        children = []
        if (after_contains[0] != "n"):
            for bag in after_contains.split(", "):
                words = bag.split(" ")
                count = int(words[0]) if words[0].isnumeric() else 0
                child_type = " ".join(words[1:3])
                children.append({"bag_name": child_type, "count": count})
        bags.append({"bag_name": bag_name, "children": children})
        if bag_name == "shiny gold":
            kids = children
    return countChildren(bags, kids)


# %% Run all
if __name__ == "__main__":
    data = load_data()

    print(part1(data))
    print(part2(data))

# %%
