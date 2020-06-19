#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
version: python 3.8
greedy.py creates lines according to greedy constraints
Michael Faber, 6087582
"""

import random as rd
import copy

from code.classes import Line
from code.algorithms.random import Random_Connections


class Greedy(Random_Connections):
    """
    Defines the Greedy algorithm
        has inheritance from Random_Connections

    parameters:
        connections     - connections in database;
        max_duration    - maximal duration for a line
        max_n_of_l      - maximal number of lines;

    methods:
       create_line      - creates a single line using greedy algorithm;
       run              - runs the algorithm a number of times
    """

    def create_line(self, uid, connection_list):
        '''
        Creates a single line using greedy algorithm

        parameters:
            uid             - unique id given to Line class;
            connection_list - list of all connections that can be used;
        '''

        # Set variables
        state = 0
        line = Line(uid)

        # Loop till broken
        while True:

            # Choose random starting point
            start_connection = rd.choice(self._connections)

            # Check if starting point has not been used yet
            if str(start_connection) in connection_list:
                connection_list.remove(str(start_connection))
                break

            # if there are no connections to start from change state to 1
            elif not connection_list:
                state = 1
                break

        # If there is a startpoint
        if state == 0:

            # Add first connection
            line.add_connection(start_connection, self._max_duration)

            # While current + shortest duration is shorter than max duration
            while (line.duration + min(line.get_all_options().keys(),
                   key=lambda x: x.duration).duration <= self._max_duration):

                # Get all options
                options = [option for sublist in line.get_begin_end_options()
                           for option in sublist]

                # Get all options that have not been ridden
                updated_options = [option for option in options if str(option)
                                   in connection_list]

                # Choose the updated option with shortest duration
                if updated_options:
                    best_option = min(updated_options,
                                      key=lambda x: x.duration)
                    connection_list.remove(str(best_option))

                # If there are no updated options stop the line
                else:
                    break

                # Add extra connection to line
                line.add_connection(best_option, self._max_duration)

        # If there are no starting options return empty line
        else:
            line = []

        return line, connection_list

    def run(self, repeat=1):
        """
        run this algorithm

        parameter:
            repeat - number of repeats to do for this algorithm;

        returns the result
        """

        # make sure repeat is an integer
        try:
            float(repeat)
        except ValueError:
            exit("RunError: please make sure you've entered a number for "
                 "the number of repeats")

        # loop for each repeat
        for run in range(repeat):
            # loop between max and min number of lines
            for n_of_l in range(self._max_n_of_l, self._min_n_of_l - 1, -1):

                # predefine lines list
                lines = []

                # create list of all connections
                connection_list = [str(connection) for connection
                                   in copy.deepcopy(self._connections)]

                # create current number of lines
                for line_index in range(n_of_l):
                    line, connection_list = \
                        self.create_line(line_index, connection_list)

                    # check for empty values
                    if not line:
                        pass
                    else:
                        lines.append(line)

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
