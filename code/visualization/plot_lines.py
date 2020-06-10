#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-
"""
version: python 3.8
plot_lines.py creates plots for input lines
Michael Faber, 6087582
"""

import sys
import os
import matplotlib.pyplot as plt
import geopandas as gpd
import math

def plot_map(stations, connections, lines, area, output_path="./output/"):
    # Create Figure and Axe
    fig = plt.figure()
    fig, ax = plt.subplots()
    plt.axis("off")

    # Setup
    if area == "Holland":
        land_color = "#00AAEE"
        marker_size = 20
        line_size = 2
    
    else: #if area == "Nationaal":
        land_color = "#EE0066"
        marker_size = 10
        line_size = 1 
    
    # Plot Background
    gpd_map(area).plot(ax=ax, color=land_color)

    # Plot all connections
    for connection in connections:
        connect_long = [station.position[0] for station in connection.section]
        connect_lat = [station.position[1] for station in connection.section]
        ax.plot(connect_lat,connect_long, linewidth=line_size, color="grey", zorder=1)

    # Plot all stations
    station_long = [station.position[0] for station in stations.values()]
    station_lat = [station.position[1] for station in stations.values()]
    #station_name = [station._name for station in stations.values()]
    ax.scatter(station_lat,station_long, s=marker_size, marker="o", color="black", zorder=2)

    # Plot all lines
    for station_line in [line.stations for line in lines]:
        line_long = [station.position[0] for station in station_line]
        line_lat = [station.position[1] for station in station_line]
        ax.plot(line_lat,line_long, linewidth=2*line_size, alpha=0.5)

    # Set aspect and save
    ax.set_aspect(aspect_ratio(station_long))
    plt.savefig(f"{output_path}Map-{area}.png", dpi=300, format="png", transparent=True)
    print(f"Map-{area} is created.")

def gpd_map(area, path="./data/shapefile/NLD_adm1.dbf"):

    try:
        assert type(area) is str
    except AssertionError:
        exit("Please enter a string")

    print(f"Searching for map of {area}.")
        
    if area == "Holland":
        # Create GeoDataFrame with the areas of Noord- and Zuid-Holland
        gdf = gpd.read_file(path)
        gdf = gdf[gdf.NAME_1.str.contains("Holland")]

    elif area == "Nationaal":
        # Create GeoDataFrame with all of the land-areas of the Netherlands
        gdf = gpd.read_file(path)
        gdf = gdf[gdf.TYPE_1=="Provincie"]

    else:
        # Try to create a lowres GeoDataFrame with given area name
        world = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
        if world.name.str.contains(area).sum() < 1:
            exit("No match to that area found. Try other name.")
        else:
            if world.name.str.contains(area).sum() == 1:
                print("Low Resolution Shapefile found.")
                gdf = world.name.str.contains(area)
            elif world.name.str.contains(area).sum() > 1:
                print(f"{world.name.str.contains(area).sum()} areas with that name found, return first result in Low Resolution. \n Try other area name.")
            

    return gdf
            

def aspect_ratio(longitude_list):
    # Adaption from: https://stackoverflow.com/questions/18873623/matplotlib-and-apect-ratio-of-geographical-data-plots
    middle_long = ((max(longitude_list)+min(longitude_list))/2)
    return 1/math.cos(math.radians(middle_long))