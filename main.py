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
import math


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

    stations, connections = load(stations_file, connections_file)

    max_duration = sum(connection.duration for connection in connections)

    min_no_of_l = math.ceil(max_duration/duration)

    runs = None

    # for n_of_l_index in range(n_of_l, min_no_of_l - 1, -1):
    lines, score = create_lines(stations, connections, duration, n_of_l)

        # if len(runs) <= 0:
        #     runs.append((lines, score))
        # elif runs[1] < score:
        #     runs.append((lines, score))

    # lines, score = runs[-1]

    plot_map(stations, connections, lines, area)

    output(lines, score)


def load_data(stations_file, connections_file):

    for item in load(stations_file, connections_file):
        print(item)
        for _ in range(10):
            print("-", end="")
        print()


def output(lines, score):
    output_writer = csv.writer(open("output/output.csv", "w"), delimiter=",")

    output_writer.writerow(["train", "stations"])

    for index, line in enumerate(lines):
        output_writer.writerow([f"train_{index + 1}",line.stations])

    output_writer.writerow(["score", score])


def create_lines(stations, connections, duration, n_of_l):

    K = 0
    tries = 0
    max_tries = 1E4
    p = 0

    best_run = None

    time = 0

    for connection in connections:
        time += connection.duration

    print(time, len(connections))

    connections = sorted(connections, key=lambda x: x.duration)

    for connection in connections:
        print(connection.duration, connection.section)

    while (p != 1):

        lines = create_random_line(stations, connections, duration, n_of_l)

        K, p = goal_function(lines, connections, n_of_l)

        tries += 1

        if not best_run:
            best_run = (lines, K, p)
        elif K > best_run[1] and p >= best_run[2]:
            best_run = (lines, K, p)

    lines, K, p = best_run

    for line in lines:
        print(line.stations)
        print(f"Duration {int(line.duration)} min")
    print("K-score", int(K))
    print(
        f"sections traversed {p*len(connections):.0f}/{len(connections):.0f}")
    print("tries", int(tries))

    return lines, K


def goal_function(lines, connections, n_of_l):

    used_connections = set()
    Min = 0

    for line in lines:
        Min += line.duration
        for connection in line.connections:
            used_connections.add(connection)

    p = len(used_connections)/len(connections)
    T = n_of_l

    return p * 10000 - (T * 100 + Min), p


def calc_state_space(stations, connections, duration, n_of_l):

    min_duration = min(connections, key=lambda x: x.duration).duration
    max_connect_per_station = len(
        max(stations.values(), key=lambda x: len(x.connections)).connections)
    connect_per_line = duration / min_duration
    state_space = n_of_l * (max_connect_per_station ** connect_per_line)

    print("Max connections per Station", max_connect_per_station)
    print("Minimal Duration", min_duration)
    print("Max connections per Line", connect_per_line)
    print("Number of Lines", n_of_l)
    print(f"State space {state_space:1.3e}")


if __name__ == "__main__":


    # import from parent directory
    #   https://stackoverflow.com/a/16985066
    PACKAGE_PARENT = '..'
    SCRIPT_DIR = os.path.dirname(os.path.realpath(
        os.path.join(os.getcwd(), os.path.expanduser(__file__))))
    sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

    from code.data_loader.load_data import load
    from code.algorithms.create_lines import create_random_line
    from code.plotting.plot_lines import plot_map

    start = time.time_ns()

    main(sys.argv[1:])

    end = time.time_ns()

    print(f"{(end-start) / 1e9} s")
