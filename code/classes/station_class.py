#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-
"""
version: python 3.8
station_class.py defines the Station class used for the database
Dani van Enk, 11823526
"""

from .connection_class import Connection


class Station():

    def __init__(self, name, x, y):
        try:
            assert type(name) is str
            x = float(x)
            y = float(y)
        except (AssertionError, ValueError):
            exit("StationInitError: please make sure the name is a string and x/y are floats")

        self._name = name
        self._longitude = x
        self._latitude = y
        self._connections = dict()

    @property
    def position(self):
        return self._latitude, self._longitude

    @property
    def connections(self):
        return self._connections

    @connections.setter
    def add_connection(self, connection):
        try:
            assert type(connection) is Connection
        except AssertionError:
            exit("StationAddConnectionError: please make sure connection is a Connection object")
        
        section = connection.section

        for station in section:
            if station is not self:
                self._connections[connection] = station

    def __repr__(self):
        return self._name
