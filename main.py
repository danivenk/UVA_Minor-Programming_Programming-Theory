#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
version: python 3.8
main.py runs the main app

authors:
    Dani van Enk, 11823526
    Michael Faber, 6087582
"""

# used imports
import sys
import csv
import matplotlib.pyplot as plt
import math

from code.data_loader.load_data import load
from code.algorithms import Random_Connections, Greedy, Hill_Climber, \
                            Simulated_Annealing
from code.visualization.plot_lines import plot_map, plot_iter_graph
from code.classes import Arg


def main(argv):
    """
    run main part of the code
    """

    # define commandline arguments
    arguments = [Arg(("-h", "--help"), "Prints this message", True),
                 Arg(("-a", "--area"), "Area run the algorithms for"),
                 Arg(("-d", "--duration"), "Max duration for one line",
                     argument_type="int"),
                 Arg(("-L", "--lines"), "Max no. of lines",
                     argument_type="int"),
                 Arg(("-r", "--repeat"), "No. of repetitions",
                     argument_type="int"),
                 Arg(("-i", "--iterations"), "No. of iterations per run", True,
                     "int"),
                 Arg(("-A", "--algorithm"), "Algorithm to run")]

    # print help function if help parameters are present or no arguments given
    if len(argv) == 0 or "-h" in argv or "--help" in argv:
        print_help(arguments)

    # create empty set for argument options
    argument_options = ()

    # add all argument aliases to argument_options
    for argument in arguments:
        argument_options += argument.aliases

    # predefine user_input dictionary
    user_input = dict()

    # go over each argument
    for arg in arguments:

        # find the corresponding given values
        for index in range(0, len(argv) - 1, 2):

            # add to user_input if value is not argument_flag
            if argv[index] in arg.aliases and \
                    argv[index + 1] not in argument_options:
                try:
                    arg.value = argv[index + 1]
                    user_input[arg.name] = arg.value
                except IndexError:
                    pass
            # if value is argument flag print help function
            elif argv[index + 1] in argument_options:
                print_help(arguments)

    # get stations/connections file paths
    stations_file = f"data/Stations{user_input['area']}.csv"
    connections_file = f"data/Connecties{user_input['area']}.csv"

    # load stations and connections
    stations, connections = load(stations_file, connections_file)

    # create lines according to user parameters
    lines, score, scores = create_lines(connections, **user_input)

    # plot the resulting line map
    plot_map(stations, connections, lines, **user_input)

    # generate the output file and plot scores
    output(lines, score, scores, **user_input)


def print_help(arguments):
    """
    print help function

    parameters:
        arguments - arguments to be printed
    """

    # print usage
    print("usage python3 main.py [options]\n")

    print("required options:")

    # print required options
    for argument in arguments:
        if not argument.optional:
            print(argument)

    print()
    print("optional options:")

    # print optional options
    for argument in arguments:
        if argument.optional:
            print(argument)

    print()

    # exit
    exit()


def output(lines_solution, score, scores, **kwargs):
    """
    generate output file and plot scores

    parameters:
        lines_solution  - lines for optimal solution;
        score           - best score for the lines;
        scores          - dictionary of all scores from the algorithm runs;
        kwargs          - the user input;
    """

    # required kwargs arguments
    required = ["area", "duration", "lines", "repeat", "algorithm"]

    # make sure kwargs requirements are defined
    for item in required:
        if item not in kwargs:
            exit("make sure you have specified the area, duration, "
                 "lines, repeat, algorithm flags")

    # create an output file
    output_writer = csv.writer(open("output/output.csv", "w"), delimiter=",")

    # write header
    output_writer.writerow(["train", "stations"])

    # add solution
    for index, line in enumerate(lines_solution):
        stations_string = ', '.join(str(station) for station in line.stations)
        output_writer.writerow([f"train_{index + 1}",
                                f"[{stations_string}]"])

    # add score
    output_writer.writerow(["score", score])

    # define algorithm
    algorithm = kwargs["algorithm"].lower()

    # create empty string
    string = ""

    # create string containing user input values
    for items in kwargs.items():
        string += f"-{'_'.join(str(item) for item in items)}"

    # plot linegraph for HC and SA, histogram for random and greedy
    if algorithm == "hill_climber" or algorithm == "simulated_annealing":
        plot_iter_graph(scores, **kwargs)
    else:
        # predefine upper bound for score
        score_upper = 0

        # plot scores in histogram
        fig = plt.figure()
        ax = fig.gca()

        # get jet color map
        cm = plt.get_cmap("jet")

        # set the color cycle to the jet color map
        ax.set_prop_cycle(color=[cm(1.*i/len(scores))
                          for i in range(len(scores))])

        # loop for the number of lines
        for n_of_l in scores:

            # get score list
            score_list = scores[n_of_l]["scores"]

            # get new upper bound score
            score_upper_new = max(score_list)

            # check if it is higher than old one
            if score_upper < score_upper_new:
                score_upper = score_upper_new

            # define bin size for Holland, Nationaal and the rest
            if kwargs["area"].lower() == "holland":
                binsize = 500
            elif kwargs["area"].lower() == "nationaal":
                binsize = 100
            else:
                binsize = 10

            # plot histogram
            plt.hist(score_list, bins=[i for i in range(0, 10000, binsize)],
                     alpha=.9, label=f"{n_of_l} lines")

        # ceil to nearest binmax
        xlim_value = math.ceil(score_upper/binsize) * binsize

        # plot setup
        ax.legend()
        plt.xlim(0, xlim_value)
        plt.ylim(0,)
        plt.xlabel("K-score")
        plt.ylabel("# of K-score solutions")
        plt.savefig(f"output/plot/Graph{string}.png")
        plt.clf()


def create_lines(connections, **kwargs):
    """
    create lines according to user parameters

    parameters:
        connections - connections in dataset;
        **kwargs    - argument dict;
    """

    # define required kwargs
    required = ["algorithm", "duration", "lines", "repeat"]

    # check if all required are present in kwargs
    for item in required:
        if item not in kwargs.keys():
            exit("make sure algorithm, duration and lines")

    # define all algorithm options
    algorithms = {"random": Random_Connections, "greedy": Greedy,
                  "hill_climber": Hill_Climber,
                  "simulated_annealing": Simulated_Annealing}

    # run the specified algorithm
    algorithm = algorithms[kwargs["algorithm"].lower()](
        connections, kwargs["duration"], kwargs["lines"])

    # if iteration is specified run multiple
    try:
        lines, K, p = algorithm.run(kwargs["repeat"], kwargs["iterations"])[0]
    except KeyError:
        lines, K, p = algorithm.run(kwargs["repeat"])[0]

    # get score
    scores = algorithm.scores

    # print stations/duration/score/coverage of solution
    for line in lines:
        print(", ".join(str(station) for station in line.stations))
        print(f"Duration {int(line.duration)} min")
    print("K-score", int(K))
    print(f"sections traversed {p*len(connections):.0f}/"
          f"{len(connections):.0f}")

    return lines, K, scores


# if name is main run main()
if __name__ == "__main__":
    main(sys.argv[1:])
