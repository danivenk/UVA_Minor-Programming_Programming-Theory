#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-
"""
version: python 3.8
create_lines.py creates lines according to the given constraints
Dani van Enk, 11823526
"""

import random as rd
import copy

from code.algorithms.random import Random_Connections


class Hill_Climber(Random_Connections):

    def __init__(self, connections, max_duration, max_n_of_l):
        super().__init__(connections, max_duration, max_n_of_l)

        self._current_state = super().run()[0]

        self._changed_lines = []

    def get_available_connections(self, lines):
        used_connections = dict()

        for line in lines:
            for connection in line.connections:
                used_connections[str(connection)] = connection
        all_connections = {str(connection): connection
                           for connection in self._connections}
        available_connections = \
            [all_connections[connection] for connection in
                all_connections.keys() - used_connections.keys()]

        return available_connections

    def ends_cut(self, state):
        line = rd.choice(state[0])

        while (line in self._changed_lines):
            line = rd.choice(state[0])

        connections = line.connections

        current_HEAD_index, direction = \
            rd.choice(line.begin_end_station_index)

        if len(connections) <= 1:
            return None

        if connections[current_HEAD_index] == \
                connections[current_HEAD_index + direction]:

            line.stations.pop(current_HEAD_index)
            line.connections.pop(current_HEAD_index)

            return state

        return None

        # if len(connections) == len(set(connections)):
        #     self._changed_lines.append(line)

    def add_missing(self, state):
        lines = state[0]

        duration_condition = \
            [line.duration < self._max_duration for line in lines]

        if state[2] < 1 and any(duration_condition):
            available_connections = self.get_available_connections(lines)

            line = rd.choice(lines)

            connection = rd.choice(available_connections)

            print(line.duration, connection.duration, self._max_duration)

            if not line.add_connection(connection,
                                       self._max_duration):
                return None

            return state

        return None

    def run(self, iterations=1, repeat=1):

        try:
            float(iterations)
            float(repeat)
        except ValueError:
            exit("RunError: please make sure you've entered a number "
                 "for the number of repeats and the number of iterations")

        print(self._current_state[1:])
        for line in self._current_state[0]:
            print(line.connections)
            print(line.stations)
            print(line.duration)

        print(self.get_available_connections(self._current_state[0]))

        for _ in range(repeat):
            for _ in range(iterations):
                state = copy.deepcopy(self._current_state)

                options = [self.ends_cut, self.add_missing]

                new_state = rd.choice(options)(state)

                if new_state:
                    state = new_state

                # ec_state = self.ends_cut(state)
                # am_state = self.add_missing(state)

                # if ec_state:
                #     state = ec_state
                # elif am_state:
                #     state = am_state

                score = self.goal_function(state[0])

                if score[0] > state[1]:
                    self._current_state = (state[0],) + score

        print(self._current_state[1:])
        for line in self._current_state[0]:
            print(line.connections)
            print(line.stations)
            print(line.duration)

        print(self.get_available_connections(self._current_state[0]))
