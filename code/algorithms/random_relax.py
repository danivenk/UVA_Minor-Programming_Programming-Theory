#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-
"""
version: python 3.8
create_lines.py creates lines according to the given constraints
Dani van Enk, 11823526
"""

import random as rd
import math

from collections import defaultdict

from code.classes import Line, Connection


class Random_Relax_Connections():

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

    def create_line(self, uid):

        line = Line(uid)

        line.add_connection(rd.choice(self._connections), self._max_duration)

        while (line.duration + min(line.get_all_options().keys(),
               key=lambda x: x.duration).duration <= self._max_duration):

            options = rd.choice(line.get_begin_end_options())

            connection = rd.choice(list(options.keys()))
            if line.add_connection(connection, self._max_duration):
                self.penalty_check(line, connection)

        return line

    def penalty_check(self, line, connection):

        try:
            assert type(line) is Line and type(connection) is Connection
        except AssertionError:
            exit("PenaltyCheckError: Make sure line is of type Line and "
                 "connection is of type Connection")

        if line.connections[-1] == connection or \
                line.connections[0] == connection:
            line.add_to_penalty(1000)

    def run(self, repeat=1):

        try:
            float(repeat)
        except ValueError:
            exit("RunError: please make sure you've entered a number for "
                 "the number of repeats")

        for run in range(repeat):
            for n_of_l in range(self._max_n_of_l, self._min_n_of_l - 1, -1):
                lines = []

                total_penalty = 0

                for line_index in range(n_of_l):
                    line = self.create_line(line_index)
                    lines.append(line)

                    total_penalty += line.penalty

                goal_function_result = self.goal_function(lines, total_penalty)

                self._result.append((lines,) + goal_function_result)
                self._scores["run"].append(run)
                self._scores["score"].append(goal_function_result[0])

            self._result = sorted(self._result, key=lambda x: x[1],
                                  reverse=True)[:5]

        return self._result
