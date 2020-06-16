#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-

import os
import sys

def main():
    # a = clss.Station("a", 1, 2)
    # b = clss.Station("b", 1, 1)
    # c = clss.Station("c", 1, 0)
    # d = clss.Station("d", 2, 1)

    # ab = clss.Connection(a, b, 5)
    # bc = clss.Connection(b, c, 10)
    # bd = clss.Connection(b, d, 10)

    # print(f"a: {a.connections}, b: {b.connections}, c: {c.connections}, d: {d.connections}")

    # line_1 = clss.Line(1)

    # print(f"{ab} {line_1.adclssonnection(ab, 200)}")
    # print(f"{bd} {line_1.adclssonnection(bd, 200)}")
    # print(f"{bc} {line_1.adclssonnection(bc, 200)}")

    # print(line_1.stations, line_1.duration)
    
    # line_2 = clss.Line(2)

    # print(f"{ab} {line_2.adclssonnection(ab, 200)}")
    # print(f"{bc} {line_2.adclssonnection(bc, 200)}")
    # print(f"{bd} {line_2.adclssonnection(bd, 200)}")
    # print(f"{bc} {line_2.adclssonnection(bc, 200)}")

    # print(line_2.stations, line_2.duration)

    # line_3 = clss.Line(3)

    # print(f"{bc} {line_3.adclssonnection(bc, 200)}")
    # print(f"{bd} {line_3.adclssonnection(bd, 200)}")

    # print(line_3.stations, line_3.duration)

    stations_file = f"data/StationsHolland.csv"
    connections_file = f"data/ConnectiesHolland.csv"

    stations, connections = load(stations_file, connections_file)

    print(stations)
    print(connections)



if __name__ == "__main__":

    # # import from parent directory
    # #   https://stackoverflow.com/a/16985066
    # PACKAGE_PARENT = '..'
    # SCRIPT_DIR = os.path.dirname(os.path.realpath(
    #     os.path.join(os.getcwd(), os.path.expanduser(__file__))))
    # sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

    import code.classes as clss
    from code.data_loader.load_data import load

    main()
