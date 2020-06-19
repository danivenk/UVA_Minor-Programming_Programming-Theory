#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
version: python 3.8
hill_climber.py defines the Hill Climbing algorithm
Dani van Enk, 11823526
"""


# used imports
import random as rd
import copy

from code.algorithms.random import Random_Connections


class Hill_Climber(Random_Connections):
    """
    Defines the Hill Climber algorithm
        has inheritance from Random_Connections

    parameters:
        connections     - connections in database;
        max_duration    - maximal duration for a line
        max_n_of_l      - maximal number of lines;

    methods:
        get_available_connections   - finds all available/not used connections;
        ends_cut                    - cuts end of random line of given state;
        add_missing                 - adds missing connections where possible;
        run                         - runs algorithm for specified values;
    """

    def __init__(self, connections, max_duration, max_n_of_l):
        """
        Initializes the Hill Climber Algorithm

        parameters:
            connections     - connections in database;
            max_duration    - maximal duration for a line
            max_n_of_l      - maximal number of lines;
        """

        # init Hill Climber from inheritance
        super().__init__(connections, max_duration, max_n_of_l)

        # get state from running inheritance
        self._current_state = super().run()[0]

        # predefining changed lines list
        self._changed_lines = []

    def get_available_connections(self, lines):
        """
        gets available connections

        parameter:
            lines - contains the used connections;

        returns available connections
        """

        # predefining used connections dictionary
        used_connections = dict()

        # loop over all lines and add used connections
        for line in lines:
            for connection in line.connections:
                used_connections[str(connection)] = connection

        # define all connections dictionary
        all_connections = {str(connection): connection
                           for connection in self._connections}

        # find the difference between all connections and used connections
        available_connections = \
            [all_connections[connection] for connection in
                all_connections.keys() - used_connections.keys()]

        return available_connections

    def ends_cut(self, state):
        """
        cuts the ends from random line at random end

        parameter:
            state - state to cut ends from;

        returns None if failed, state if successful
        """

        # get random line
        line = rd.choice(state[0])

        # make sure line is not already changed
        while (line in self._changed_lines):
            line = rd.choice(state[0])

        # get line connections
        connections = line.connections

        # get random end of line
        current_HEAD_index, direction = \
            rd.choice(line.begin_end_station_index)

        # make sure line has more than one connection
        if len(connections) <= 1:
            return None

        # check if duplicate connections present at the chosen end
        if connections[current_HEAD_index] == \
                connections[current_HEAD_index + direction]:

            # remove duplicate connection
            line.stations.pop(current_HEAD_index)
            line.connections.pop(current_HEAD_index)

            return state

        return None

    def add_missing(self, state):
        """
        add missing connections to state where possible

        parameter:
            state - state to add missing connections to;

        returns None if failed, state if successful
        """

        # get lines from state
        lines = state[0]

        # get duration condition for each line, duration < max duration
        duration_condition = \
            [line.duration < self._max_duration for line in lines]

        # if there are connections missing
        #   duration condition can be satisfied
        if state[2] < 1 and any(duration_condition):

            # get available connections
            available_connections = self.get_available_connections(lines)

            # choose random line
            line = rd.choice(lines)

            # choose random missing connection
            connection = rd.choice(available_connections)

            # if connection can't be added return None
            if not line.add_connection(connection,
                                       self._max_duration):
                return None

            return state

        return None

    def run(self, iterations=1):
        """
        run this algorithm

        parameters:
            iterations  - number of tries to change the current state
                (default 1);
        """

        # make sure iterations is a integer
        try:
            int(iterations)
        except ValueError:
            exit("RunError: please make sure you've entered a integer "
                 "for the number of iterations")

        # print(self._current_state[1:])
        # for line in self._current_state[0]:
        #     print(line.connections)
        #     print(line.stations)
        #     print(line.duration)

        # print(self.get_available_connections(self._current_state[0]))

        # loop for each iteration
        for _ in range(iterations):

            # create a copy of the current state
            state = copy.deepcopy(self._current_state)

            # define options
            options = [self.ends_cut, self.add_missing]

            # choose random option
            new_state = rd.choice(options)(state)

            # make sure option worked
            if new_state:
                state = new_state

            # get new score
            score = self.goal_function(state[0])

            # check if score has been improved
            if score[0] > state[1]:
                self._current_state = (state[0],) + score

        # print(self._current_state[1:])
        # for line in self._current_state[0]:
        #     print(line.connections)
        #     print(line.stations)
        #     print(line.duration)

        # print(self.get_available_connections(self._current_state[0]))
