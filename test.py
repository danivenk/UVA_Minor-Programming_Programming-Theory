#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-

import os
import sys
import random as rd

from code.classes import Line

def main():
    a = clss.Station("a", 1, 2)
    b = clss.Station("b", 1, 1)
    c = clss.Station("c", 1, 0)
    d = clss.Station("d", 2, 1)

    ab = clss.Connection(a, b, 5)
    bc = clss.Connection(b, c, 10)
    bd = clss.Connection(b, d, 10)
    da = clss.Connection(d, a, 2)

    stations = [a, b, c, d]

    connections = [ab, bc, bd, da]


    random = Random_Connections(connections, 50, 1)

    random.run()

    # for _ in range(10):

        # random.create_line(0)

    # print(f"a: {a.connections}, b: {b.connections}, c: {c.connections}, d: {d.connections}")

    # line_1 = clss.Line(1)


    # print(f"{ab} {line_1.add_connection(ab, 200)}")
    # print(f"{bd} {line_1.add_connection(bd, 200)}")
    # print(f"{bc} {line_1.add_connection(bc, 200)}")
        

    # for station in line_1.stations:
    #     print(station)
    # print(line_1.duration)

    # print("=" * 10)
    
    # line_2 = clss.Line(2)

    # print(f"{ab} {line_2.add_connection(ab, 200)}")
    # print(f"{bc} {line_2.add_connection(bc, 200)}")
    # print(f"{bd} {line_2.add_connection(bd, 200)}")
    # print(f"{bc} {line_2.add_connection(bc, 200)}")

    # for station in line_2.stations:
    #     print(station)
    # print(line_2.duration)

    # print("=" * 10)

    # line_3 = clss.Line(3)

    # print(f"{bc} {line_3.add_connection(bc, 200)}")
    # print(f"{bd} {line_3.add_connection(bd, 200)}")
    # print(f"{bc} {line_3.add_connection(bc, 200)}")
    # print(f"{bd} {line_3.add_connection(bd, 200)}")

    # for station in line_3.stations:
    #     print(station)
    # print(line_3.duration)

    # stations_file = f"data/StationsHolland.csv"
    # connections_file = f"data/ConnectiesHolland.csv"

    # stations, connections = load(stations_file, connections_file)

    # line = Line(0)

    # line.add_connection(rd.choice(connections), 120)

    # for _ in range(100000):
        
    #     option = rd.choice(line.get_begin_end_options())

    #     line.add_connection(rd.choice(list(option.keys())), 120)

    # print("YEH")

    # for _ in range(100000):
    #     line = Line(0)

    #     for _ in range(100):
    #         line.add_connection(rd.choice(connections), 120)

    #     station = rd.choice(list(stations.values()))
    #     for connection, stationto in station.connections.items():
    #         if station == stationto:
    #             print(station, connection, stationto)


    # random = Random_Connections(connections, 120, 7)

    # for station in stations.values():

    # for _ in range(1000000):
        # print("="*10)

    # for _ in range(10):
    #     line = Line(0)

    #     for _ in range(2):
    #         line.add_connection(rd.choice(connections), 120)

    #     for station in line.stations:
    #         print("hihi", station)
        
    #     print("="*10)

    #     for option in line.get_begin_end_options():
    #         for connection in option:
    #             print(option[connection])

    #         print("="*10)

    # random.create_line(0)

    # for station in random.create_line(0).stations:
    #     print("station", station)

    # print(random.run(10000))


    # for n_of_l, lines in runs.items():
    #     print(n_of_l, "number of lines")
    #     print("=" * 5)
    #     for uid, line in enumerate(lines):
    #         print(uid, f"{line.duration:g}", line)
    #     print()




if __name__ == "__main__":

    import code.classes as clss
    from code.data_loader.load_data import load
    from code.algorithms.random import Random_Connections

    main()
