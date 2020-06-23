"""
version: python 3.8
plot_lines.py contains methods that can be used
    to plot multiple lines on a map

methods:
    plot_map        - plot all the lines on a map and save as png-file;
    gpd_map         - returns Geopandas DataFrame of given area;
    line_coords     - returns start and end values of connection;
    ofset_dict      - returns dictionairy with connections and their ofsets;
    aspect_ratio    - returns ratio of latitude and longitude for use in map;
    random_color    - returns random RGB-values to make color.

authors:
    Dani van Enk, 11823526
    Michael Faber, 6087582
"""

# imports
import math
import random

import matplotlib.pyplot as plt
import geopandas as gpd

from wcag_contrast_ratio import rgb
from PIL import ImageColor
from collections import defaultdict


def plot_map(stations, connections, lines, area, output_path="./output/"):
    """
    Plot all the lines on a Map and save as png-file

    parameters:
        stations        - all stations in database;
        connections     - all connections in database;
        lines           - the lines that are plotted;
        area            - geographical area of lines;
        output_path     - folder where plot is saved;
    """

    # Create Figure and Axe
    fig = plt.figure(dpi=600)
    fig, ax = plt.subplots()
    plt.axis("off")

    # Format Options of Holland and others
    if area == "Holland":
        land_color = tuple(i/255. for i in ImageColor.getrgb("#0AE"))
        marker_size = 10
        line_size = 1

    else:  # if area == "Nationaal":
        land_color = tuple(i/255. for i in ImageColor.getrgb("#E06"))
        marker_size = 5
        line_size = 1

    # predefine used colors
    used_colors = []

    # Plot Background using geopandas
    gpd_map(area).plot(ax=ax, color=land_color)

    # For-loop to get each individual connection between stations
    for connection in connections:

        # Create tuples of x and y using coordinates of begin- and end station
        connect_long = [station.position[0] for station in connection.section]
        connect_lat = [station.position[1] for station in connection.section]

        # Plot connection
        ax.plot(connect_long, connect_lat, linewidth=line_size, color="grey",
                alpha=0.5, zorder=1)

    # Create lists of x and y values from the coordinates of all stations
    station_long = [station.position[0] for station in stations.values()]
    station_lat = [station.position[1] for station in stations.values()]

    # Calculate the ratio between the longitude and latitude
    ratio = aspect_ratio(station_lat)

    # Create a dictionary of connections that need ofset
    ofset = ofset_dict(lines)

    # For-loop to get each single line
    for line_number in range(len(lines)):

        # generate random color
        color = random_color()

        # generate new color the contrast is high enough no double colors
        while (rgb(color, land_color) >= 10 and color not in used_colors):
            color = random_color()

        # add color to used color
        used_colors.append(color)

        # For-loop to get each connection in a line
        for connection in list(set(lines[line_number].connections)):

            # Get the adjusted longitude and latitude
            longitude, latitude = line_coords(connection, ofset, ratio,
                                              line_number)

            # Plot connection
            ax.plot(longitude, latitude, c=color, linewidth=line_size,
                    zorder=2)

    # Plot all stations
    ax.scatter(station_long, station_lat, s=marker_size, marker="o",
               color="black", zorder=3)

    # Set aspect using ratio value
    ax.set_aspect(ratio)

    # Save plot to png file
    plt.savefig(f"{output_path}Map-{area}.png", dpi=300, format="png",
                transparent=True)
    print(f"Map-{area} is created.")


def gpd_map(area, path="./data/shapefile/NLD_adm1.dbf"):
    """
    Return Geopandas DataFrame of area

    parameters:
        area    - geographical area that needs to be mapped
        path    - path of shapfiles needed to draw in high quality
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
        gdf = gdf[gdf.TYPE_1 == "Provincie"]

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
            elif results.sum() > 1:
                print(f"{results.sum()} areas with that name found, return "
                      "first result in Low Resolution. \nTry other area name.")
                gdf = results.head(1)

    return gdf


def line_coords(connection, ofset_dict, ratio, line_number, line_size=1,
                line_distance=0.01):
    """
    Give start and end values of connection, with ofset if it is needed.

    parameters:
        connection      - single connection between two stations;
        ofset_dict      - dictionary containing all ofset information;
        ratio           - the ratio between longitude and lattitude;
        line_number     - uid of the line
        line_size       - width of the line being drawed
        line_distance   - ofset distance
    """

    # Create lists with longitude/latitude values of end points of connection
    longitude = [connection.section[0].position[0],
                 connection.section[1].position[0]]
    latitude = [connection.section[0].position[1],
                connection.section[1].position[1]]

    # Check if other lines are using same conncection
    other_lines = ofset_dict[line_number][connection]

    # If no other lines are using the same connection make no adjustments
    if other_lines == 0:
        adjusted_longitude = longitude
        adjusted_latitude = latitude

    # If other lines are using the same connection
    else:

        # Set new location where connection will come
        ofset_state = round((1-(2.0001*(other_lines % 2)))*other_lines/2)

        # calculate angle between the x-axis and the linesection
        angle = math.atan((latitude[1] - latitude[0]) /
                          (longitude[1] - longitude[0]))

        # calculate the offset for x and y,
        #   line_distance must be the linewidth and margin
        xoffset = -ofset_state * line_distance * ratio * math.sin(angle)
        yoffset = ofset_state * line_distance * math.cos(angle)

        # calculate the adjusted long/lat values
        adjusted_longitude = [x + xoffset for x in longitude]
        adjusted_latitude = [y + yoffset for y in latitude]

    return (adjusted_longitude, adjusted_latitude)


def ofset_dict(lines):
    """
    Creates a nested dictionary where for every line the connections
    are showed that have been in a line before and how many times.

    parameter:
        lines   - all lines that are plotted

    returns dictionary with ofset for every connection in every line
    """

    # Create empty dictionary
    ofset = {}

    # for every line(number) create a defaultdict with an integer
    for line_number in range(len(lines)):
        ofset[line_number] = defaultdict(int)

        # Loop through all the previous lines
        for previous_line_number in range(line_number):

            # Create empty list
            used_connections = []

            # Loop through all the connections in a single line
            for connection in lines[line_number].connections:

                # If the connection in previous line and not counted before
                if (connection in lines[previous_line_number].connections) and\
                        (connection not in used_connections):

                    # Count previous line and put in not count list
                    ofset[line_number][connection] += 1
                    used_connections.append(connection)

    return(ofset)


def aspect_ratio(latitude_list):
    """
    Returns ratio of latitude and longitude for use in map

    parameter:
        latitude_list  - list of all latitudes used in the plot
    """

    # Find middle of map by dividing sum of lowest and highest latitude by 2
    middle_long = ((max(latitude_list)+min(latitude_list))/2)

    # Return calculated ratio
    # Formula from: https://stackoverflow.com/q/18873623
    return 1/math.cos(math.radians(middle_long))


def random_color():
    """
    Return random RGB-values to make color.
    """

    return (random.random(), random.random(), random.random())
