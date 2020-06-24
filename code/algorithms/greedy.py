"""
version: python 3.8
greedy.py creates lines according to greedy constraints

authors:
    Dani van Enk, 11823526
    Michael Faber, 6087582
"""

# used imports
import random as rd
import copy
import progressbar as pbar

from collections import defaultdict

from code.classes import Line
from code.algorithms import Random_Connections


class Greedy(Random_Connections):
    """
    Defines the Greedy algorithm
        has inheritance from Random_Connections

    parameters:
        connections     - connections in database;
        max_duration    - maximal duration for a line
        max_n_of_l      - maximal number of lines;

    methods:
       choose_start         - returns start connection that has not been used;
       choose_best_option   - returns best option according to method;
       add_options          - add as much greedy options as possible to line;
       create_line          - creates a single line using greedy algorithm;
       run                  - runs the algorithm a number of times
    """

    def choose_start(self, connection_list):
        """
        Returns random starting connection that has not been used

        parameter:
            connection_list     - list of all connections that are not used
        """

        # Choose random start connection
        start_connection = rd.choice(self._connections)

        # While start connection is already used
        while str(start_connection) not in connection_list:

            # Choose random start connection
            start_connection = rd.choice(self._connections)

        # Delete chosen start connection from connection list
        connection_list.remove(str(start_connection))

        return start_connection, connection_list

    def choose_best_option(self, line, connection_list,
                           method="min", one_time=False):
        """
        chooses best option according to different methods

        parameters:
            line                - line where best option must be chosen for;
            connection_list     - list with all possible connections;
            method              - method used to choose best option;
            one_time            - if a connection can be used one time;

        returns a single connection that can be added to line
        """

        # Get all options
        options = [option[0] for option in line.get_all_options().values()]

        if one_time:
            # Get all options that have not been ridden
            options = [option for option in options if str(option)
                       in connection_list]

        if options:

            # If method is min, return min
            if method == "min":
                return min(options, key=lambda x: x.duration)

            # If method is max, return max
            elif method == "max":
                return min(options, key=lambda x: x.duration)

            # If method is minconnections, return min connections
            elif method == "minconnections":
                return min(options, key=lambda x: len(x.connections))

            # If method is maxconnections, return max connections
            elif method == "maxconnections":
                return max(options, key=lambda x: len(x.connections))

            # If other method is specified, print error
            else:
                print("Give a valid method")

        return False

    def add_options(self, line, connection_list):
        """
        Add as much greedy options as possible to line

        parameters:
            line            - line with only start connection added;
            connection_list - list with all possible connections;

        returns line with new options and updated connection_list
        """

        # While current + shortest duration is shorter than max duration
        while (line.duration + min(line.get_all_options().values(),
               key=lambda x: x[0].duration)[0].duration <= self._max_duration):

            # Choose the best option
            best_option = self.choose_best_option(line, connection_list)

            # If there is a best option delete from connection list
            if str(best_option) in connection_list:
                connection_list.remove(str(best_option))

            # If there are no best option stop the line
            elif not best_option:
                break

            # Add extra connection to line
            line.add_connection(best_option, self._max_duration)

        return line, connection_list

    def create_line(self, connection_list):
        '''
        Creates a single line using greedy algorithm

        parameters:
            connection_list - list of all connections that can be used;

        returns completed line and connection_list for extra runs
        '''

        # Set variables
        line = Line()

        # If there is a startpoint
        if connection_list:

            # Add startpoint
            start_connection, connection_list = \
                    self.choose_start(connection_list)

            # Add first connection
            line.add_connection(start_connection, self._max_duration)

            # Add other connections
            line, connection_list = self.add_options(line, connection_list)

        # If there are no starting options return empty line
        else:
            line = []

        return line, connection_list

    def run(self, repeat=1):
        """
        run this algorithm

        parameter:
            repeat - number of repeats to do for this algorithm;

        returns the result
        """

        # make sure repeat is an integer
        try:
            float(repeat)
        except ValueError:
            exit("RunError: please make sure you've entered a number for "
                 "the number of repeats")

        # print running parameters
        print(f"Runing, Greedy {repeat} times")

        # reset the result list and scores dict
        self._result = []
        self._scores = defaultdict(lambda: defaultdict(list))

        # define the progress bar widgets
        bar_widgets = [pbar.Bar("#", "[", "]"), " ", pbar.ETA()]

        # define the max value
        maxval = repeat * (self._max_n_of_l - self._min_n_of_l + 1)

        # create the progress bar and start
        bar = pbar.ProgressBar(maxval=maxval, widgets=bar_widgets).start()

        # initiate step to 0
        step = 0

        # loop for each repeat
        for run in range(repeat):
            # loop between max and min number of lines
            for n_of_l in range(self._max_n_of_l, self._min_n_of_l - 1, -1):

                # predefine lines list
                lines = []

                # create list of all connections
                connection_list = [str(connection) for connection
                                   in copy.deepcopy(self._connections)]

                # create current number of lines
                for _ in range(n_of_l):
                    line, connection_list = \
                        self.create_line(connection_list)

                    # check for empty values
                    if not line:
                        pass
                    else:
                        lines.append(line)

                # get score
                goal_function_result = self.goal_function(lines)

                # add result to results attribute and save score
                self._result.append((lines,) + goal_function_result)
                self._scores[n_of_l]["runs"].append(run)
                self._scores[n_of_l]["scores"].append(goal_function_result[0])

                # update progress bar
                step += 1
                bar.update(step)

            # save the 5 best results
            self._result = sorted(self._result, key=lambda x: x[1],
                                  reverse=True)[:5]

        # finish the progress bar
        bar.finish()

        return self._result
