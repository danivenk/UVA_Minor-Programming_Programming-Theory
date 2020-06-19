#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-
"""
version: python 3.8
main.py runs the main app
Dani van Enk, 11823526
"""

# used imports
import sys
import csv
import time


class Arg():
    def __init__(self, aliases, description, optional=False,
                 argument_type="str"):
        self._aliases = aliases
        self._description = description
        self._argument_type = argument_type
        self._value = None
        self._optional = optional

    @property
    def aliases(self):
        return self._aliases

    @property
    def description(self):
        return self._description

    @property
    def argument_type(self):
        return self._argument_type

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if self._argument_type == "int":
            try:
                self._value = int(value)
            except ValueError:
                exit("value is not a integer")
        else:
            self._value = value

    @property
    def optional(self):
        return self._optional

    @property
    def name(self):
        for alias in self._aliases:
            if "--" in alias:
                return alias.lstrip("--")

        for alias in self._aliases:
            if "-" in alias:
                return alias.lstrip("-")

        return alias

    def __str__(self):
        return f'{", ".join(self._aliases):<20} {self.description}'


def main(argv):

    arguments = [Arg(("-h", "--help"), "Prints this message", True),
                 Arg(("-a", "--area"), "Area run the algorithms for"),
                 Arg(("-d", "--duration"), "Max duration for one line",
                     argument_type="int"),
                 Arg(("-L", "--lines"), "Max no. of lines",
                     argument_type="int"),
                 Arg(("-r", "--repeat"), "No. of repetitions", True, "int"),
                 Arg(("-i", "--iterations"), "No. of iterations per run", True,
                     "int"),
                 Arg(("-A", "--algorithm"), "Algorithm to run")]

    if len(argv) == 0 or "-h" in argv or "--help" in argv:
        print_help(arguments)

    argument_options = ()

    for argument in arguments:
        argument_options += argument.aliases

    user_input = dict()

    for arg in arguments:
        for index in range(0, len(argv) - 1, 2):
            if argv[index] in arg.aliases and \
                    argv[index + 1] not in argument_options:
                try:
                    arg.value = argv[index + 1]
                    user_input[arg.name] = arg.value
                except IndexError:
                    pass
            elif argv[index + 1] in argument_options:
                print_help(arguments)

    stations_file = f"data/Stations{user_input['area']}.csv"
    connections_file = f"data/Connecties{user_input['area']}.csv"

    stations, connections = load(stations_file, connections_file)

    lines, score = create_lines(stations, connections, **user_input)

    plot_map(stations, connections, lines, user_input['area'])

    output(lines, score)


def print_help(arguments):
    print("usage ./main.py [options]\n")

    print("required options:")

    for argument in arguments:
        if not argument.optional:
            print(argument)

    print()
    print("optional options:")

    for argument in arguments:
        if argument.optional:
            print(argument)

    print()

    exit()


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
        output_writer.writerow([f"train_{index + 1}",
                                f"[{station for station in line.stations}]"])

    output_writer.writerow(["score", score])


def create_lines(stations, connections, **kwargs):

    required = ["algorithm", "duration", "lines"]

    for item in required:
        if item not in kwargs.keys():
            exit("make sure algorithm, duration and lines")

    algorithms = {"random": Random_Connections, "greedy": Greedy}

    algorithm = algorithms[kwargs["algorithm"].lower()](
        connections, kwargs["duration"], kwargs["lines"])

    try:
        lines, K, p = algorithm.run(kwargs["repeat"])[0]
    except KeyError:
        lines, K, p = algorithm.run()[0]

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
    from code.algorithms import Random_Connections
    from code.algorithms.greedy import Greedy
    from code.visualization.plot_lines import plot_map

    start = time.time_ns()

    main(sys.argv[1:])

    end = time.time_ns()

    print(f"{(end-start) / 1e9} s")
