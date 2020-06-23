# RailNL - Shibayama (芝山)
-------------------------------------------
In the [RailNL](https://theorie.mprog.nl/cases/railnl) case, we're trying to optimize the line planning of trains. The case contains two sets of CSV-files, one for the stations and connections in Noord- and Zuid-Holland, and one for the stations and connections of the Netherlands. The goal is to get for both areas a covering network with a maximum of maxLines and where the duration of every line is not longer than maxTime.


|       Area      | nStations | nConnections | maxTime | maxLines |
|----------------:|:---------:|:------------:|:-------:|:--------:|
|   **Holland**   |     22    |      32      |   120   |    7     |
| **Netherlands** |     45    |      89      |   180   |    20    |

The quality of the solution can be measured using the following formula:

<img src="https://render.githubusercontent.com/render/math?math=Q=p\cdot10000-(%23Lines\cdot100%2BTotalTime)">

Where *p* is the percentage of the connections covered (between 0 and 1), *#Lines* is the number of lines used in the solution and *TotalTime* is the sum of the times of every line.


## Instructions

### Installation

The code used is completely written in Python 3.8 and all packages needed to run this program can be found in *requirements.txt*. You can use pip to install these packages with:

```
python3 -m pip install -r requirements.txt
```

Or use conda:

```
conda install --file requirements.txt
```

### Usage
To run this program you could use the function main.py that has four required input arguments and two optional. First the name of an area (-a) is needed. You could use "Holland" to calculate the lines for Noord- and Zuid-Holland and "Nationaal: to calculate the lines for the Netherlands. The second argument needed (-d) is the Maximum number of minutes that a train can ride on a line. The third argument (-L) is the number of lines the function needs to calculate. The final required input argument (-A) is the algorithm that is going to be used to create the lines. The algorithms that can be used are "random", "greedy" and "hc".

The first optional option (-r) is the amount of runs an algorithm must be used. More runs might give higher scores. The second optional option (-i) is the number of iterations the Hill Climber uses in every run.

```
usage python3 main.py [options]

required options:
-a, --area           Area run the algorithms for
-d, --duration       Max duration for one line
-L, --lines          Max no. of lines
-A, --algorithm      Algorithm to run

optional options:
-h, --help           Prints this message
-r, --repeat         No. of repetitions
-i, --iterations     No. of iterations per run
```

When filled in, it will look something like this:

```
python3 main.py -a "Holland" -d 120 -L 7 -A "random" -r 1000
```

### Output

When the function is started, it will return all the lines and number of minutes they take, a quality score of the lines combined, an output csv-file and an output map as png-file.

An example of terminal output of the above function is:

   <details><summary>Click to see Terminal Output</summary>
    <pre>
    Haarlem, Heemstede-Aerdenhout, Haarlem, Amsterdam Sloterdijk, Zaandam, Hoorn, Alkmaar, Den Helder
    Duration 115 min
    Den Haag Centraal, Gouda, Alphen a/d Rijn, Leiden Centraal, Heemstede-Aerdenhout, Haarlem, Beverwijk, Haarlem, Amsterdam Sloterdijk, Amsterdam Centraal
    Duration 119 min
    Alphen a/d Rijn, Leiden Centraal, Den Haag Centraal, Delft, Den Haag Centraal, Leiden Centraal, Alphen a/d Rijn, Gouda, Den Haag Centraal
    Duration 115 min
    Amsterdam Zuid, Amsterdam Sloterdijk, Haarlem, Amsterdam Sloterdijk, Amsterdam Centraal, Amsterdam Sloterdijk, Zaandam, Castricum, Beverwijk, Zaandam, Amsterdam Sloterdijk, Amsterdam Centraal
    Duration 118 min
    Rotterdam Centraal, Schiedam Centrum, Delft, Den Haag Centraal, Gouda, Rotterdam Alexander, Rotterdam Centraal, Schiedam Centrum, Delft, Schiedam Centrum, Rotterdam Centraal, Dordrecht, Rotterdam Centraal
    Duration 119 min
    Leiden Centraal, Heemstede-Aerdenhout, Leiden Centraal, Schiphol Airport, Amsterdam Zuid, Amsterdam Amstel, Amsterdam Zuid, Amsterdam Amstel, Amsterdam Centraal, Amsterdam Amstel, Amsterdam Centraal, Amsterdam Sloterdijk, Amsterdam Centraal, Amsterdam Sloterdijk
    Duration 119 min
    K-score 8337
    sections traversed 27/28
    7.4045667 s
    Searching for map of Holland.
    Map-Holland is created.
    </pre>
   </details>

And an example of the output map will look like:

<img src="doc/img/Example.png" alt="Output Map Example" />

### Structure
All the important folders and files are structured below:

- **/code**:contains all code.
    - **/code/algorithms**: contains code to draw lines.
    - **/code/classes**: contains all classes.
    - **/code/data_loader**: contains code to load data.
    - **/code/visualization**: contains code to plot results.
- **/data**: contains csv-files of RailNL case.
    - **/data/shapefile**: contains shapefile to draw (parts of) the Netherlands.
- **/output**: contains (examples of) output-files.
    - **/output/plot**: contains output-plots.

## Authors
- Dani van Enk
- Michael Faber