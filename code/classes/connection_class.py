#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-
"""
version: python 3.8
connection_class.py defines the Connection class used for the database
Dani van Enk, 11823526
"""

import code.classes as cls


class Connection():

    def __init__(self, start, end, duration):
        try:
            assert type(start) is cls.Station and type(end) is cls.Station
            duration = float(duration)
        except (AssertionError, ValueError):
            exit("ConnectionInitError: please make sure the start and end parameters are a Station"
                 " object\n and duration is a number")

        self._start = start
        self._end = end
        self._duration = duration

        start.add_connection = self
        end.add_connection = self

    @property
    def duration(self):
        return self._duration

    @duration.setter
    def set_duration(self, duration):
        if duration < 0:
            raise ValueError(f"{duration} is smaller than 0")
        else:
            self._duration = duration

    @property
    def section(self):
        return self._start, self._end

    def __repr__(self):
        return f"{self._start} - {self._end}"