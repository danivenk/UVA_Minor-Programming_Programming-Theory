#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-
"""
version: python 3.8
load_data.py loads the data from data/
    (only when the files have the correct name style)
Dani van Enk, 11823526
"""

# used imports
import sys
import os
import csv
import pandas as pd


class Station():

    def __init__(name, x, y):
        self.name = name
        self.position = {"x": x, "y": y}


def main(argv):

    if len(argv) != 1:
        exit("usage ./load_data.py <area>")

    PATH_Connections = f"data/Connecties{argv[0]}.csv"
    PATH_Stations = f"data/Stations{argv[0]}.csv"

    try:

        # get csv reader object from the datafile
        datafile_connections = open(PATH_Connections, "r", encoding="utf-8")
        connections_file = csv.reader(datafile_connections, delimiter=",")

        connections_header = next(connections_file)

    except FileNotFoundError:
        exit(f"{PATH_Connections} not found")

    try:

        # get csv reader object from the datafile
        datafile_stations = open(PATH_Stations, "r", encoding="utf-8")
        stations_file = csv.reader(datafile_stations, delimiter=",")

        stations_header = next(stations_file)

    except FileNotFoundError:
        exit(f"{PATH_Stations} not found")

    stations = []

    for station in station_file:
        stations.append(station[0], )


if __name__ == "__main__":
    main(sys.argv[1:])
