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
from code.classes import Line

def create_random_line(stations, connections, duration, n_of_l):

    lines = []

    for uid in range(n_of_l):
        line = Line(uid)

        random_connection = rd.choice(connections)
        while line.add_connection(random_connection, duration):
            # print(line.duration, line.stations[-1], line.stations[0], random_connection)
            random_connection = rd.choice(connections)

        lines.append(line)

    return lines