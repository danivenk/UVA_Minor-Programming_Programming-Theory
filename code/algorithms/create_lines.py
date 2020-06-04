#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-
"""
version: python 3.8
create_lines.py creates lines according to the given constraints
Dani van Enk, 11823526
"""

import sys
import os
import random as rd

from code.data_loader.load_data import load
from code.classes.data_classes import Line

def create_random_lines(stations, connections, duration, n_of_l):

    lines = []

    for uid in range(n_of_l):
        line = Line(uid)

        random_connection = rd.choice(connections)
        while line.add_connection(random_connection, duration):
            random_connection = rd.choice(connections)

        lines.append(line)

    lines = sorted(lines, key=lambda x:x.duration)

    for line in lines:
        print(f"Duration: {line.duration}")
        print(f"Start: {line.stations[0]} - End: {line.stations[-1]}")
        # for station in line.stations:
        #     print(station)
