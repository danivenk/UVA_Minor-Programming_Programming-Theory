#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-
"""
version: python 3.8
main.py runs the main app
Dani van Enk, 11823526
"""

# used imports
import sys
import os
import csv
import time


def main(argv):

    if len(argv) != 3 or "-h" in argv or "--help" in argv:
        exit("usage ./create_lines.py <area> <duration> <no_of_lines>")

    area = argv[0]

    try:
        duration = int(argv[1])
        n_of_l = int(argv[2])
    except ValueError:
        exit("make sure duration and no_of_lines are integers")

    stations_file = f"data/Stations{area}.csv"
    connections_file = f"data/Connecties{area}.csv"

    create_lines(stations_file, connections_file, duration, n_of_l)


def load_data(stations_file, connections_file):

    for item in load(stations_file, connections_file):
        print(item)
        for _ in range(10):
            print("-", end="")
        print()


def create_lines(stations_file, connections_file, duration, n_of_l):

    stations, connections = load(stations_file, connections_file)

    create_random_lines(stations, connections, duration, n_of_l)
    


if __name__ == "__main__":


    # import from parent directory
    #   https://stackoverflow.com/a/16985066
    PACKAGE_PARENT = '..'
    SCRIPT_DIR = os.path.dirname(os.path.realpath(
        os.path.join(os.getcwd(), os.path.expanduser(__file__))))
    sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

    from code.classes.data_classes import *
    from code.data_loader.load_data import load
    from code.algorithms.create_lines import create_random_lines

    start = time.time_ns()

    main(sys.argv[1:])

    end = time.time_ns()

    print(f"{(end-start) / 1e9}")
