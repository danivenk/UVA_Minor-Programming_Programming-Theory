#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-
"""
version: python 3.8
station_class.py defines the Station class used for the database
Dani van Enk, 11823526
"""

# import used classes
import code.classes as clss


class Station():
    """
    the Station class defines a station

    parameters:
        name    - name of the station;
        x       - longitude position of the station;
        y       - latitiude position of the station;

    properties:
        position        - returns the longitude and latitude of the station;
        connections     - returns all all connections of this station;
            setter: connection is of type Conenction
    """

    def __init__(self, name, x, y):
        """
        initialize a station

        paramters:
            name    - name of the station;
            x       - longitude position of the station;
            y       - latitude position of the station;
        """

        # make sure x/y are floats and name is a string
        try:
            assert type(name) is str
            x = float(x)
            y = float(y)
        except (AssertionError, ValueError):
            exit("StationInitError: please make sure the name is a string "
                 "and x/y are floats")

        # define name, longitude, latitude and connections attirbutes
        self._name = name
        self._longitude = x
        self._latitude = y
        self._connections = dict()

    @property
    def position(self):
        """
        return the longitude/latitude position tuple
        """

        return self._longitude, self._latitude

    @property
    def connections(self):
        """
        return the connections of this station
        """

        # for connection, stationto in self._connections.items():
        #     if self == stationto:
        #         print("from: ", self, "to: ", stationto)

        return self._connections

    @connections.setter
    def add_connection(self, connection):
        """
        adds a connection to this stop

        parameter:
            connection - connection to be added;
        """

        # make sure connection is of type Connection
        try:
            assert type(connection) is clss.Connection
        except AssertionError:
            exit("StationAddConnectionError: please make sure connection is "
                 "a Connection object")
        
        # define the section of this connection
        section = connection.section

        # make sure connection is valid for this station
        if self not in section:
            exit("StationAddConnectionError: station not in connection")

        # add the station of this connection which is not this station
        for station in section:
            if station is not self:
                self._connections[connection] = station

    def __repr__(self):
    #     """
    #     return the correct representation of the Station class
    #     """

    #     return f"{self._name} at position " \
    #         f"(long: {self._longitude}, lat: {self._latitude})"
    
    # def __str__(self):
    #     """
    #     return the string format of the Station class
    #     """

        return self._name
