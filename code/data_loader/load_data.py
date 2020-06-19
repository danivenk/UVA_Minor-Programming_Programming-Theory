#!/usr/bin/env python3
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
    """
    loads data files into database

    parameters:
        stations_file    - path to the stations file;
        connections_file - path to the connections file;

    returns stations dictionary and connection list
    """

    # make sure stations file exists
    try:

        # get csv reader object from the datafile
        stations_reader = csv.reader(
            open(stations_file, "r", encoding="utf-8"), delimiter=",")

        # skip header
        next(stations_reader)

    except FileNotFoundError:
        exit(f"{stations_file} not found")

    # make sure connections file exists
    try:

        # get csv reader object from the datafile
        connections_reader = csv.reader(
            open(connections_file, "r", encoding="utf-8"), delimiter=",")

        # skip header
        next(connections_reader)

    except FileNotFoundError:
        exit(f"{connections_file} not found")

    # add stations and connections to database
    stations = {name: Station(name, lat, long)
                for name, lat, long in stations_reader}
    connections = [Connection(stations[start], stations[end], duration)
                   for start, end, duration in connections_reader]

    return stations, connections
