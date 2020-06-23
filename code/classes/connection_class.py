#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
version: python 3.8
connection_class.py defines the Connection class used for the database
Dani van Enk, 11823526
"""

# import used classes
import code.classes as clss


class Connection():
    """
    the Connection class defines a connection between 2 stations

    parameters:
        start       - starting station;
        end         - end station;
        duration    - duration between stations;

    properties:
        duration    - returns the duration between stations;
            setter condition: duration of more than 0
        section     - returns the start and end stations;

    method:
        other - get other station in connection;
    """

    # define general unique identifier
    guid = 0

    def __init__(self, start, end, duration):
        """
        initialize a Connection

        parameters:
            start       - starting station;
            end         - end station;
            duration    - duration between stations;
            cid         - return the connection id;
        """

        # make sure start and end are of Station type and duration is a number
        try:
            assert type(start) is clss.Station and type(end) is clss.Station
            duration = float(duration)
        except (AssertionError, ValueError):
            exit("ConnectionInitError: please make sure the start and end "
                 "parameters are a Station object\n and duration is a number")

        # define start, end and duration attributes
        self._start = start
        self._end = end
        self._duration = duration
        self._id = self.guid

        # increase general unique identifier
        Connection.guid += 1

        # add connection to start and end stations
        start.add_connection(self)
        end.add_connection(self)

    @property
    def duration(self):
        """
        returns the duration of this connection
        """

        return self._duration

    @duration.setter
    def duration(self, duration):
        """
        sets duration of this connection

        parameters:
            duration - duration between stations;
        """

        # make sure duration is bigger than 0
        if duration < 0:
            raise ValueError(f"{duration} is smaller than 0")
        else:
            self._duration = duration

    @property
    def section(self):
        """
        return the start/end station tuple
        """

        return self._start, self._end

    @property
    def cid(self):
        """
        return the connection id
        """

        return self._id

    def __repr__(self):
        """
        return the correct representation of the Connection class
        """

        return f"Section: {self._start} - {self._end} " \
               f"(Duration: {self._duration})"

    def __str__(self):
        """
        return the string format of the Connection class
        """

        return f"{self._start} - {self._end}"
