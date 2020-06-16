#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-
"""
version: python 3.8
load_data.py defines the load function to load data from data/
    (only when the files have the correct name style)
Dani van Enk, 11823526
"""

# used imports
import csv
from code.classes import Station, Connection


def load(stations_file, connections_file):

    PATH_Stations = stations_file
    PATH_Connections = connections_file

    try:

        # get csv reader object from the datafile
        stations_reader = csv.reader(
            open(PATH_Stations, "r", encoding="utf-8"), delimiter=",")

        next(stations_reader)

    except FileNotFoundError:
        exit(f"{PATH_Stations} not found")

    try:

        # get csv reader object from the datafile
        connections_reader = csv.reader(
            open(PATH_Connections, "r", encoding="utf-8"), delimiter=",")

        next(connections_reader)

    except FileNotFoundError:
        exit(f"{PATH_Connections} not found")

    stations = {name: Station(name, lat, long) for name, lat, long in stations_reader}
    connections = [Connection(stations[start], stations[end], duration)
                   for start, end, duration in connections_reader]

    return stations, connections
