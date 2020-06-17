#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_connections(station):
    print(f"{bcolors.HEADER}{station}{bcolors.ENDC}")
    for connection, station_ in station.connections.items():
        print(f"{connection} {bcolors.HEADER}{station_}{bcolors.ENDC}")


# for station in self.stations:
#     print_connections(station)

def check_validity(connections, station):
    for station_ in connections.values():
        if station == station_:
            print_connections(station)
            exit("ValidationError: Something went wrong")
