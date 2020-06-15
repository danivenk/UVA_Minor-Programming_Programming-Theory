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
from collections import defaultdict
import random

def plot_map(stations, connections, lines, area, output_path="./output/"):
    """
    Plot all the lines on a Map and save as png-file
    """

    # Create Figure and Axe
    fig = plt.figure()
    fig, ax = plt.subplots()
    plt.axis("off")

    # Format Options of Holland and others
    if area == "Holland":
        land_color = "#00AAEE"
        marker_size = 10
        line_size = 1
    
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
        ax.plot(connect_lat,connect_long, linewidth=line_size, color="grey", alpha=0.5, zorder=1)

    # Create lists of x and y values from the coordinates of all stations
    station_long = [station.position[0] for station in stations.values()]
    station_lat = [station.position[1] for station in stations.values()]

    # Calculate the ratio between the latitude and longitude
    ratio = aspect_ratio(station_long)
    
    # Create a dictionary of connections that need ofset
    ofset = ofset_dict(lines)

    # For-loop to get each single line
    for line_number in range(len(lines)):

        # Set color for line
        color = random_color()
        
        # For-loop to get each connection in a line
        for connection in list(set(lines[line_number].connections)):
            
            # Get the adjusted latitude and longitude
            latitude, longitude = line_coords(connection, ofset, ratio, line_number)
  
            # Plot connection
            ax.plot(latitude, longitude, c=color, linewidth=line_size, zorder=2)
            #print(latitude, longitude)

    # Plot all stations
    ax.scatter(station_lat,station_long, s=marker_size, marker="o", color="black", zorder=3)

    # Set aspect using ratio value
    ax.set_aspect(ratio)

    # Save plot to png file
    plt.savefig(f"{output_path}Map-{area}.png", dpi=300, format="png", transparent=True)
    print(f"Map-{area} is created.")

def gpd_map(area, path="./data/shapefile/NLD_adm1.dbf"):
    """
    Return Geopandas DataFrame of area
    """

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

def line_coords(connection, ofset_dict, ratio, line_number, line_size=1, line_distance=0.008):
    """
    Give start and end values of connection, with ofset if it is needed.
    """

    # Create two lists with latitude and longitude values of begin and end of connection
    latitude = [connection.section[0].position[1], connection.section[1].position[1]]
    longitude =  [connection.section[0].position[0], connection.section[1].position[0]]

    # Check if other lines are using same conncection
    other_lines =  ofset_dict[line_number][connection]

    # If no other lines are using the same connection make no adjustments
    if other_lines == 0:
        adjusted_latitude = latitude
        adjusted_longitude = longitude

    # If other lines are using the same connection
    else:

        # Set new location where connection will come
        ofset_state = round((1-(2.0001*(other_lines%2)))*other_lines/2)

        # Use ratio to calculate line distance for latitude
        latitude_distance = line_distance * ratio

        # If latitude is larger than longitude, set ofset to longitude
        if abs(latitude[0]-latitude[1]) >= (abs(longitude[0]-longitude[1])):
            adjusted_longitude = [y + (ofset_state*line_size*line_distance) for y in longitude]
            adjusted_latitude = latitude
        
        # If latitude is smaller than longitude, set ofset to latitude
        else:
            adjusted_latitude = [x + (ofset_state*line_size*latitude_distance) for x in latitude]
            adjusted_longitude = longitude

    return (adjusted_latitude, adjusted_longitude)

def ofset_dict(lines):
    """
    Creates a nested dictionary where for every line the connections
    are showed that have been in a line before and how many times.
    """

    # Create empty dictionary
    ofset = {}
    
    # for every line(number) create a defaultdict with an integer
    for line_number in range (len(lines)):
        ofset[line_number] = defaultdict(int)

        # Loop through all the previous lines
        for previous_line_number in range(line_number):

            # Create empty list
            used_connections = []

            # Loop through all the connections in a single line
            for connection in lines[line_number].connections:
                
                # If the connection is in a previous line and has not been counted before
                if (connection in lines[previous_line_number].connections) and (connection not in used_connections):
                    
                    # Count previous line and put in not count list
                    ofset[line_number][connection] += 1
                    used_connections.append(connection)

    return(ofset)

def aspect_ratio(longitude_list):
    """ 
    Return the correct ratio of longitude and latitude for use in map 
    """

    # Find middle of map by dividing sum of lowest and highest longitude by 2
    middle_long = ((max(longitude_list)+min(longitude_list))/2)

    # Return calculated ratio
    # Formula from: https://stackoverflow.com/q/18873623
    return 1/math.cos(math.radians(middle_long))

def random_color():
    """
    Return random RGB-values to make color.
    """
    return (random.random(), random.random(), random.random())