#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
version: python 3.8
astar.py uses A* algorithm to give back fastest line between stations
Michael Faber, 6087582
"""

from geopy import distance

from code.classes import Line


class A_Star():
    """
    the A_Star class is a collection of parameters, properties and methods
        to find the fastest line between two stations using an A* algorithm.

    parameters:
        connections         - all connections that can be used in a line;
        max_duration        - maximal duration of the line in minutes;
        result              - result or list of results of the algorithm;
        choices             - dictionary containing all starting points;
        number_of_results   - number of results that will be returned;
        speed               - minimal time in minutes per km;

    property:
        result              - returns result or list of results;
        speed               - returns speed as a float number;

    methods:
        update_result       - updates result according to number_of_results;
        time_per_km         - returns lowest duration divided by distance;
        station_distance    - returns distance between two stations in km;
        copy_connections    - copies connections from one line to another;
        choose_best_option  - returns best option for chosen method;
        add_choice          - adds choice to choices;
        new_line            - creates new line and adds to choices;
        create_line         - returns shortest line(s) between two stations;
    """

    def __init__(self, connections, max_duration, number_of_results=1):
        """
        initialize A_Star

        parameters:
            connections         - all connections that can be used in a line;
            max_duration        - maximal duration of the line in minutes;
            number_of_results   - number of results that will be returned;
        """

        self._connections = connections
        self._max_duration = max_duration
        self._result = []
        self._choices = dict()
        self._number_of_results = number_of_results
        self._speed = self.time_per_km()

    @property
    def result(self):
        return self._result

    @result.setter
    def result(self, value):
        self._result = value

    def update_result(self, best_option):
        """
        Update result according the maximum number of results

        parameters:
            best_option    - line that is best option from A to B;
        """
        if self._number_of_results == 1:
            self.result = best_option

        else:
            # Add best line to results for number_of_results times
            self._result.append(best_option)

    @property
    def speed(self):
        return self._speed

    def time_per_km(self):
        """
        Gives back the fastest time a train in connections does over 1 km.
        """

        # Create empty list for time per km for every connection
        minutes_per_km_list = []

        # For every connection set station 1 and 2
        for connection in self._connections:

            station1 = connection.section[0]
            station2 = connection.section[1]

            # Calculate minutes per km by dividing the time of
            # the connection by the distance between stations
            minutes_per_km = connection.duration / self.station_distance(
                             station1, station2)

            # Add to list
            minutes_per_km_list.append(minutes_per_km)

        # return lowest value in list
        return min(minutes_per_km_list)

    def station_distance(self, station1, station2):
        """
        Calculate distance between two stations using geopy

        parameters:
            station1    - station of Station class;
            station2    - station of Station class;
        """

        return distance.distance(station1.position, station2.position).km

    def copy_connections(self, new_line, old_line):
        """
        Copy all connections from one line to the other

        parameters:
            new_line    - line where the connections will be added to;
            old_line    - line where the connections will be copied from;
        """
        for old_connection in old_line.connections:
            new_line.add_connection(old_connection,
                                    self._max_duration)

    def choose_best_option(self, method="min"):
        """
        returns best option for chosen method

        parameter:
            method  - method used (min, max, minconnections, maxconnections);
        """

        # If method is min, return min
        if method == "min":
            return min(self._choices, key=self._choices.get)

        # If method is max, return max
        elif method == "max":
            return max(self._choices, key=self._choices.get)

        # If method is minconnections, return min connections
        elif method == "minconnections":
            return min(self._choices, key=lambda x: len(x.connections))

        # If method is maxconnections, return max connections
        elif method == "maxconnections":
            return max(self._choices, key=lambda x: len(x.connections))

        # If other method is specified, print error
        else:
            print("Give a valid method")

    def add_choice(self, line, station2):
        """
        Calculates penalty time and adds line to choices

        parameters:
            line        - line that will be added to choices
            station2    - the end station where the line needs to go to
        """

        # Add minimal duration to get to station2
        line.penalty = self.station_distance(
                        line.stations[-1], station2) * self.speed

        # Add line to choices with sum of duration and
        # minimal duration if less than max duration
        if line.duration + line.penalty <= self._max_duration:
            self._choices[line] = line.duration + line.penalty

    def new_line(self, connection, line, best_option, station2):
        """
        Creates copy of best_option, add new connection and add to choices

        parameters:
            connection  - connection that is going to be added;
            line        - line that will be updated;
            best_option - old line that will be copied;
            station2    - end station line is going to;
        """

        # If there are connections in best_option
        if best_option.connections:

            # If connection is not same as last connection of best option
            if connection != best_option.connections[-1]:

                # Copy all connections from best_option to line
                self.copy_connections(line, best_option)

                # Add new connection
                if line.duration + connection.duration <= self._max_duration:
                    line.add_connection(connection, self._max_duration)

                    # Add line to choices
                    self.add_choice(line, station2)

        else:

            # Add new connection
            line.add_connection(connection, self._max_duration)

            # Add line to choices
            self.add_choice(line, station2)

    def create_line(self, station1, station2):
        """
        Returns line(s) between two stations with the shortest duration
            using the A* algorithm

        parameters:
            station1    - station where pathfinding starts;
            station2    - station where pathfinding is going to;
        """

        # Set counters
        c = 0
        uid = 0

        # Set variables
        self.result = []
        self._choices = dict()
        total_duration = self.station_distance(station1, station2) * self.speed

        # If total_duration is shorter or equal to max_duration, run function
        if total_duration <= self._max_duration:

            # Create empty line with minimal duration
            line = Line(uid, station1)
            self._choices[line] = total_duration

            # While there are still choices
            while self._choices:

                # Choose the option with lowest corrected duration
                best_option = self.choose_best_option("max")

                # If it an empty line add first connection
                if uid == 0:
                    station = station1

                else:
                    station = best_option.stations[-1]

                # If the last station in the best line is the same as station2
                if station == station2:
                    self.update_result(best_option)

                    # Add one to counter to get to desired number of results
                    c += 1
                    if c == self._number_of_results:
                        break

                else:

                    # Create a new line for every connection of the station
                    for connection in station.connections:
                        uid += 1
                        line = Line(uid, station1)

                        self.new_line(connection, line, best_option, station2)

                # Delete the line used for calculations from options
                del self._choices[best_option]

        # Return result
        return self.result
