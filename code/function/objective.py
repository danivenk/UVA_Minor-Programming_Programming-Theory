#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-
"""
version: python 3.8
objective.py defines the objective function used in this program
Dani van Enk, 11823526
"""


def goal_function(lines, connections, n_of_l, penalty=0):

    used_connections = set()
    Min = penalty

    for line in lines:
        Min += line.duration
        for connection in line.connections:
            used_connections.add(connection)

    p = len(used_connections)/len(connections)
    T = n_of_l

    return p * 10000 - (T * 100 + Min), p
