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

    def __init__(self, name, x, y):
        self.name = name
        self.position = {"x": x, "y": y}

    def __repr__(self):
        return f"{self.name}, long: {self.position['x']} lat: {self.position['y']}"


class Connection():

    def __init__(self, station1, station2, duration):
        self.stations = {"start": station1, "end": station2}
        self.duration = duration

    def __repr__(self):
        return f"{self.stations['start'].name} - {self.stations['end'].name} duration:{self.duration}"


# class Line():

#     def __init__(self):
#         self.stations = []

#     @property
#     def duration(self):
#         duration = 0

#         for index in range(len(self.stations) - 2):
#             duration += 

#     def add_section(self, duration)


def main(argv):
    
    if len(argv) != 1:
        exit("usage ./load_data.py <area>")
    
    stations, stations_df, connections, connections_df = load_data(argv[0])


def load_data(area):
    PATH_Connections = f"data/Connecties{area}.csv"
    PATH_Stations = f"data/Stations{area}.csv"

    try:
        connections_df = pd.read_csv(PATH_Connections, index_col=None, header=0)
    except FileNotFoundError:
        exit(f"{PATH_Connections} not found")

    try:
        stations_df = pd.read_csv(PATH_Stations, index_col=None, header=0)
    except FileNotFoundError:
        exit(f"{PATH_Stations} not found")

    stations = dict()

    for row in stations_df.itertuples():
        stations[row.station] = Station(row.station, row.x, row.y)

    connections = []

    for row in connections_df.itertuples():
        connections.append(Connection(stations[row.station1], stations[row.station2], row.distance))

    return stations, stations_df, connections, connections_df
    

if __name__ == "__main__":
    main(sys.argv[1:])
