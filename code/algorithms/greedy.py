#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-
"""
version: python 3.8
greedy.py creates lines according to the given constraints
Michael Faber, 6087582
"""

import random as rd
import math
import copy
from collections import defaultdict

from code.classes import Line
from code.function.objective import goal_function


class Greedy():

    def __init__(self, connections, max_duration, max_n_of_l):
        self._connections = connections
        self._max_duration = max_duration
        self._max_n_of_l = max_n_of_l
        self._min_n_of_l = math.ceil(sum(connection.duration for connection
                                     in connections)/max_duration)
        self._result = []
        self._scores = defaultdict(list)

    @property
    def result(self):
        return self._result

    @property
    def scores(self):
        return self._scores

    def create_line(self, uid, connection_list):
        '''
        Creates a single line using greedy algorithm
        '''

        state = 0
        line = Line(uid)

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

        try:
            float(repeat)
        except ValueError:
            exit("RunError: please make sure you've entered a number for "
                 "the number of repeats")

        for run in range(repeat):
            for n_of_l in range(self._max_n_of_l, self._min_n_of_l - 1, -1):
                lines = []

                connection_list = [str(connection) for connection
                                   in copy.deepcopy(self._connections)]
                for line_index in range(n_of_l):
                    line, connection_list = \
                        self.create_line(line_index, connection_list)
                    if not line:
                        pass
                    else:
                        lines.append(line)

                goal_function_result = \
                    goal_function(lines, self._connections, n_of_l)

                self._result.append((lines,) +
                                    goal_function(lines,
                                                  self._connections, n_of_l))
                self._scores["run"].append(run)
                self._scores["score"].append(goal_function_result[0])

            self._result = sorted(self._result, key=lambda x: x[1],
                                  reverse=True)[:5]

        return self._result
