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
    """Plot all the lines on a Map and save as png-file"""

    # Create Figure and Axe
    fig = plt.figure()
    fig, ax = plt.subplots()
    plt.axis("off")

    # Format Options of Holland and others
    if area == "Holland":
        land_color = "#00AAEE"
        marker_size = 20
        line_size = 2
    
    else: #if area == "Nationaal":
        land_color = "#EE0066"
        marker_size = 10
        line_size = 1 
    
    # Plot Background using geopandas
    gpd_map(area).plot(ax=ax, color=land_color)

    # For-loop to get each individual connection between stations
    for connection in connections:

        # Create tuples of x and y using coordinates of begin- and end station
        connect_long = [station.position[0] for station in connection.section]
        connect_lat = [station.position[1] for station in connection.section]

        # Plot connection
        ax.plot(connect_lat,connect_long, linewidth=line_size, color="grey", zorder=1)

    # Create lists of x and y values from the coordinates of all stations
    station_long = [station.position[0] for station in stations.values()]
    station_lat = [station.position[1] for station in stations.values()]

    # Plot all stations
    ax.scatter(station_lat,station_long, s=marker_size, marker="o", color="black", zorder=2)

    # For-loop to get stations of each line
    for station_line in [line.stations for line in lines]:

        # Create lists of x and y values of the route of the line
        line_long = [station.position[0] for station in station_line]
        line_lat = [station.position[1] for station in station_line]

        # Plot line
        ax.plot(line_lat,line_long, linewidth=2*line_size, alpha=0.5)

    # Use list of longitudes from stations to set correct aspect ratio
    ax.set_aspect(aspect_ratio(station_long))

    # Save plot to png file
    plt.savefig(f"{output_path}Map-{area}.png", dpi=300, format="png", transparent=True)
    print(f"Map-{area} is created.")

def gpd_map(area, path="./data/shapefile/NLD_adm1.dbf"):
    """Return Geopandas DataFrame of area"""

    # Make sure area is a string
    try:
        assert type(area) is str
    except AssertionError:
        exit("Please enter a string")

    print(f"Searching for map of {area}.")
    
    if area == "Holland":

        # Create GeoDataFrame from shapefile of the Netherlands
        gdf = gpd.read_file(path)

        # Select only Noord- and Zuid-Holland
        gdf = gdf[gdf.NAME_1.str.contains("Holland")]

    elif area == "Nationaal":

        # Create GeoDataFrame from shapefile of the Netherlands
        gdf = gpd.read_file(path)

        # Select all of the land-areas of the Netherlands
        gdf = gdf[gdf.TYPE_1=="Provincie"]

    else:

        # Create GeoDataFrame from lowres shapefile of the world
        world = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
        
        # Search for area in world GeoDataFrame
        results = world.name.str.contains(area)

        # If no match is found stop function
        if results.sum() == 0:
            exit("No match to that area found. Try other name.")
        
        else:

            # If one match is found, select result 
            if results.sum() == 1:
                print("Low Resolution Shapefile found.")
                gdf = results
            
            # If multiple matches are found, select first result
            elif result.sum() > 1:
                print(f"{result.sum()} areas with that name found, return first result in Low Resolution. \n Try other area name.")
                gdf = results.head(1)

    return gdf
            

def aspect_ratio(longitude_list):
    """ Return the correct ratio of longitude and latitude for use in map """

    # Find middle of map by dividing sum of lowest and highest longitude by 2
    middle_long = ((max(longitude_list)+min(longitude_list))/2)

    # Return calculated ratio
    # Formula from: https://stackoverflow.com/q/18873623
    return 1/math.cos(math.radians(middle_long))