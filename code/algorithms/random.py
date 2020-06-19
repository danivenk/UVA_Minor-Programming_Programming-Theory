#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
version: python 3.8
random.py defines the Random algorithm
Dani van Enk, 11823526
"""

# used imports
import random as rd
import math

from collections import defaultdict

from code.classes import Line


class Random_Connections():
    """
    Defines the Random algorithms

    parameters:
        connections     - connections in database;
        max_duration    - max duration for the lines;
        max_n_of_l      - max number of lines;

    properties:
        result  - returns the result for this algorithm;
        scores  - returns the scores of this algorithm;

    methods:
        create_line     - creates a line for this algorithm;
        goal_function   - defines the goal function;
        run             - runs this algorithm;
    """

    def __init__(self, connections, max_duration, max_n_of_l):
        """
        initialize the random algorithm

        parameters:
            connections     - connections in database;
            max_duration    - max duration for the lines;
            max_n_of_l      - max number of lines;
        """

        self._connections = connections
        self._max_duration = max_duration
        self._max_n_of_l = max_n_of_l

        # define minimum number of lines
        self._min_n_of_l = math.ceil(sum(connection.duration for connection
                                     in connections)/max_duration)

        # predefine result and scores attribute
        self._result = []
        self._scores = defaultdict(lambda: defaultdict(list))

    @property
    def result(self):
        """
        returns the result for this algorithm
        """

        return self._result

    @property
    def scores(self):
        """
        returns the scores of this algorithm
        """

        return self._scores

    def create_line(self, uid):
        """
        create a line for this algorithm

        parameter:
            uid - unique id for a line;
        """

        # create an empty line
        line = Line(uid)

        # add an random begin connection
        line.add_connection(rd.choice(self._connections), self._max_duration)

        # while there can still be added connections do this
        while (line.duration + min(line.get_all_options().keys(),
               key=lambda x: x.duration).duration <= self._max_duration):

            # get random options from begin or end of this line
            options = rd.choice(line.get_begin_end_options())

            # add random connection from options to line
            line.add_connection(rd.choice(list(options.keys())),
                                self._max_duration)

        return line

    def goal_function(self, lines, penalty=0):
        """
        define the goal function

        parameters:
            lines   - lines to calculate the goal function for;
            penalty - penalties for the lines (default is 0);
        """

        # predefine used connections and number of minutes to the penalty value
        used_connections = set()
        Min = penalty

        # for each line in lines find used connections and add minutes
        for line in lines:
            Min += line.duration
            for connection in line.connections:
                used_connections.add(connection)

        # calculate the coverage and define the number of lines
        p = len(used_connections)/len(self._connections)
        T = len(lines)

        return p * 10000 - (T * 100 + Min), p

    def run(self, repeat=1):
        """
        run this algorithm

        parameter:
            repeat - number of repeats to do for this algorithm;

        returns the result
        """

        # make sure repeat is an interger
        try:
            int(repeat)
        except ValueError:
            exit("RunError: please make sure you've entered a int "
                 "for the number of repeats")

        # loop for each repeat
        for run in range(repeat):
            # loop between max and min number of lines
            for n_of_l in range(self._max_n_of_l, self._min_n_of_l - 1, -1):

                # predefine lines list
                lines = []

                # create current number of lines
                for line_index in range(n_of_l):
                    lines.append(self.create_line(line_index))

                # get score
                goal_function_result = self.goal_function(lines)

                # add result to results attribute and save score
                self._result.append((lines,) + goal_function_result)
                self._scores[n_of_l]["runs"].append(run)
                self._scores[n_of_l]["scores"].append(goal_function_result[0])

            # save the 5 best results
            self._result = sorted(self._result, key=lambda x: x[1],
                                  reverse=True)[:5]

        return self._result
