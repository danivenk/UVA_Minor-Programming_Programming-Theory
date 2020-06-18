#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-
"""
version: python 3.8
astar.py gives the fastest line(s) between two stations
Michael Faber, 6087582
"""

from geopy import distance
from collections import defaultdict

from code.classes import Line


class A_Star():

    def __init__(self, connections, stations,
                 max_duration, number_of_results=1):

        self._connections = connections
        self._stations = stations
        self._max_duration = max_duration
        self._result = []
        self._choices = defaultdict(float)
        self._number_of_results = number_of_results

    @property
    def result(self):
        return self._result

    @result.setter
    def set_result(self, value):
        self._result = value

    def time_per_km(self):
        """
        Gives back the fastest time a train
        in connections does over 1 km.
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
        """

        return distance.distance(station1.position, station2.position).km

    def create_line(self, station1, station2):
        """
        Returns line(s) between two stations with the shortest duration
        """

        # Set counters
        c = 0
        uid = 0

        # Set variables
        speed = self.time_per_km()
        total_duration = self.station_distance(station1, station2) * speed

        # If total_duration is shorter or equal to max_duration, run function
        if total_duration <= self._max_duration:

            # Create empty line with minimal duration
            line = Line(uid)
            self._choices[line] = total_duration

            # While there are still choices
            while self._choices:

                # Choose the option with lowest corrected duration
                best_option = min(self._choices, key=self._choices.get)

                # If it an empty line add first connection
                if uid == 0:
                    starting_station = station = station1
                    start = True

                else:
                    station = best_option.stations[-1]
                    starting_station = None
                    start = False

                # If the last station in the best line is the same as station2
                if station == station2:

                    if self._number_of_results == 1:
                        self._result = best_option
                        break

                    else:
                        # Add best line to results for number_of_results times
                        self._result.append(best_option)
                        c += 1
                        if c == self._number_of_results:
                            break

                else:

                    # Create a new line for every connection of the station
                    for connection in station.connections:
                        uid += 1
                        line = Line(uid)

                        if not start:
                            # Add the connections made before to the new line
                            line.add_connection(best_option.connections[0],
                                                self._max_duration, station1)
                            for old_connection in best_option.connections[1:]:
                                line.add_connection(old_connection,
                                                    self._max_duration)

                        line.add_connection(connection, self._max_duration,
                                            starting_station)

                        # Add minimal duration to get to station2
                        line._penalty = (self.station_distance(
                            connection.other(station), station2) * speed)

                        # Add line to choices with sum of duration
                        # and calculated minimal duration
                        self._choices[line] = line.duration + line.penalty

                # Delete the line used for calculations from options
                del self._choices[best_option]

        # Return result
        return self._result
