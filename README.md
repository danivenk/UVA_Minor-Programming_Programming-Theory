# RailNL - Shibayama (芝山)
-------------------------------------------
In the [RailNL](https://theorie.mprog.nl/cases/railnl) case, we're trying to optimize the line planning of trains. The case contains two sets of CSV-files, one for the stations and connections in Noord- and Zuid-Holland, and one for the stations and connections of the Netherlands. The goal is to get for both areas a covering network with a maximum of maxLines and where the duration of every line is not longer than maxTime.


|       Area      | nStations | nConnections | maxTime | maxLines |
|----------------:|:---------:|:------------:|:-------:|:--------:|
|   **Holland**   |     22    |      32      |   120   |    7     |
| **Netherlands** |     45    |      89      |   180   |    20    |

The quality of the solution can be measured using the following formula:

$$ Q = p \cdot 10000 -(#Lines \cdot 100 + TotalTime) $$

Where $p$ is the percentage of the connections covered (between 0 and 1), $#Lines$ is the number of lines used in the solution and $TotalTime$ is the sum of the times of every line.


## Instructions

### Installation

The code used is completely written in Python 3.8 and all packages needed to run this program can be found in *requirements.txt*. You can use pip to install these packages with:

```
pip3 install -r requirements.txt
```

Or use conda:

```
conda install --file requirements.txt
```

### Usage
To run this program you could use the function main.py that needs 3 input arguments. First the name of an area is needed. You could use 'Holland' to calculate the lines for Noord- and Zuid-Holland and 'Nationaal' to calculate the lines of the Netherlands. The second argument needed is the Maximum number of minutes that a train can ride on a line. The last argument is the number of lines the function needs to calculate.

```
python3 main.py str:area int:maxminutes int:#lines
```

When filled in, it will look like:

```
python3 main.py "Holland" 120 7
```

When the function is started, it will return all the lines and number of minutes they take, a quality score of the lines combined, an output csv-file and an output map as png-file.

### Structure
All the important folders and files are structured below:

- **/code**:contains all code.
    - **/code/algorithms**: contains code to draw lines.
    - **code/classes**: contains all classes.
    - **code/data_loader**: contains code to load data.
    - **code/visualization**: contains code to plot results.
- **/data**: contains csv-files of RailNL case.
    - **/data/shapefile**: contains shapefile to draw (parts of) the Netherlands.
- **/output**: contains (examples of) output-files.
    

## Authors
- Dani van Enk
- Michael Faber