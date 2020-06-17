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


def create_lines(stations, connections, duration, n_of_l, algorithm="greedy"):

    random = Random_Connections(connections, duration, n_of_l)
    greedy = Greedy(connections, duration, n_of_l)
    
    if algorithm == "random":
        lines, K, p = random.run(10000)[0]
    elif algorithm == "greedy":
        lines, K, p = greedy.run(10000)[0]

    for line in lines:
        print(", ".join(str(station) for station in line.stations))
        print(f"Duration {int(line.duration)} min")
    print("K-score", int(K))
    print(
        f"sections traversed {p*len(connections):.0f}/{len(connections):.0f}")

    return lines, K


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

    from code.data_loader.load_data import load
    from code.algorithms import Random_Connections, Random_Relax_Connections
    from code.algorithms.greedy import Greedy
    from code.visualization.plot_lines import plot_map

    start = time.time_ns()

    main(sys.argv[1:])

    end = time.time_ns()

    print(f"{(end-start) / 1e9} s")
