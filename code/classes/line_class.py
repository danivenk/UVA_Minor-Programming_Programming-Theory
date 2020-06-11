#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-
"""
version: python 3.8
line_class.py defines the Line classe used for the database
Dani van Enk, 11823526
"""

# import used classes
import code.classes as cls


class Line():
    """
    the Line class defines a combination of connections (and thus also stations)

    paramters:
        id              - is the lineid;
        connections     - all connections present in this line;
        stations        - the stations of this line in the correct order;

    properties:
        duration        - returns duration of this line;
        no_of_stations  - returns number of station in this line;
        stations        - returns stations list of this line;
        connections     - returns connections list of this line;

    method:
        add_connection - adds connection to line if valid
            true if added correctly false if not;
    """

    def __init__(self, _id):
        """
        initialize the Line class

        parameter:
            id - Line-ID;
        """
        
        self._id = _id
        self._connections = []
        self._stations = []

    @property
    def duration(self):
        """
        returns the duration of this line
        """

        # predefine the duration to 0
        _duration = 0

        # loop over all the connections of this line and add to the duration
        for connection in self._connections:
            _duration += connection.duration
        
        # make sure the duration is 0 or more
        if _duration < 0:
            raise ValueError(f"{_duration} is smaller than 0")
        else:
            return _duration

    @property
    def no_of_stations(self):
        """
        return the number of stations of this line
        """

        return len(self._stations)

    @property
    def stations(self):
        """
        return the stations list
        """
        
        return self._stations

    @property
    def connections(self):
        """
        return the connections list
        """

        return self._connections

    def add_connection(self, connection, max_duration):
        """
        adds a connection to the connections list if the connection is valid

        parameters:
            connection      - connection to be added;
            max_duration    - max duration of this line;

        returns True if the ###########################
        """
        
        # make sure connection is of type Conenction and max_duration is a number
        try:
            assert type(connection) is cls.Connection
            max_duration = float(max_duration)
        except (AssertionError, ValueError):
            exit("LineAddConnectionError: please make sure the connection "
                 "you're adding is a connction object\n "
                 "and max_duration is a number")

        # check if the connection to be added makes the duration more than max
        if self.duration + connection.duration > max_duration:
            return False
        else:

            # if line is empty add whole connection
            if len(self._stations) == 0:
                for station in connection.section:
                    self._stations.append(station)
                self._connections.append(connection)
            
            # if not add it where it's posisble
            else:
                # define the stations at the end of the current line
                current_start = self._stations[-1]
                current_end = self._stations[0]
                
                # check if it must be added to the start or at the end of the line
                if connection in current_start.connections:
                    next_station = current_start.connections[connection]
                    self._stations.append(next_station)
                    self._connections.append(connection)
                elif connection in current_end.connections:
                    previous_station = current_end.connections[connection]
                    self._stations.insert(0, previous_station)
                    self._connections.append(connection)

        return True
