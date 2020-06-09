#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-
"""
version: python 3.8
line_class.py defines the Line classe used for the database
Dani van Enk, 11823526
"""

from .connection_class import Connection


class Line():

    def __init__(self, _id):
        self._id = _id
        self._connections = []
        self._stations = []

    @property
    def duration(self):
        _duration = 0
        for connection in self._connections:
            _duration += connection.duration
        
        if _duration < 0:
            raise ValueError(f"{_duration} is smaller than 0")
        else:
            return _duration

    @property
    def no_of_stations(self):
        return len(self._stations)

    @property
    def stations(self):
        return self._stations

    @property
    def connections(self):
        return self._connections

    def add_connection(self, connection, max_duration):
        
        try:
            assert type(connection) is Connection
            max_duration = float(max_duration)
        except (AssertionError, ValueError):
            exit("LineAddConnectionError: please make sure the connection you're adding is a connction"
                 "object\n and max_duration is a number")

        if self.duration + connection.duration > max_duration:
            return False
        else:
            if len(self._stations) == 0:
                for station in connection.section:
                    self._stations.append(station)
                self._connections.append(connection)
            else:
                current_start = self._stations[-1]
                current_end = self._stations[0]

                # if connection in self._connections:
                #     return True
                # elif len(current_start.connections) == 1 and len(current_end.connections) == 1:
                #     return False
                
                if connection in current_start.connections:
                    next_station = current_start.connections[connection]
                    self._stations.append(next_station)
                    self._connections.append(connection)
                elif connection in current_end.connections:
                    previous_station = current_end.connections[connection]
                    self._stations.insert(0, previous_station)
                    self._connections.append(connection)

        return True
