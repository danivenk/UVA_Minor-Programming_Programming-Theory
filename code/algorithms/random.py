"""
version: python 3.8
random.py defines the Random algorithm

authors:
    Dani van Enk, 11823526
    Michael Faber, 6087582
"""

# used imports
import random as rd
import math
import progressbar as pbar

from collections import defaultdict

from code.classes import Line


class Random_Connections():
    """
    Defines the Random algorithms

    parameters:
        connections     - connections in database;
        max_duration    - max duration for the lines;
        max_n_of_l      - max number of lines;

    properties:
        result  - returns the result for this algorithm;
        scores  - returns the scores of this algorithm;

    methods:
        create_line     - creates a line for this algorithm;
        goal_function   - defines the goal function;
        run             - runs this algorithm;
    """

    def __init__(self, connections, max_duration, max_n_of_l):
        """
        initialize the random algorithm

        parameters:
            connections     - connections in database;
            max_duration    - max duration for the lines;
            max_n_of_l      - max number of lines;
        """

        self._connections = connections
        self._max_duration = max_duration
        self._max_n_of_l = max_n_of_l

        # define minimum number of lines
        self._min_n_of_l = math.ceil(sum(connection.duration for connection
                                     in connections)/max_duration)

        # predefine result and scores attribute
        self._result = []
        self._scores = defaultdict(lambda: defaultdict(list))

    @property
    def result(self):
        """
        returns the result for this algorithm
        """

        return self._result

    @property
    def scores(self):
        """
        returns the scores of this algorithm
        """

        return self._scores

    def create_line(self):
        """
        create a line for this algorithm

        returns a randomly created line
        """

        # create an empty line
        line = Line()

        # add an random begin connection
        line.add_connection(rd.choice(self._connections), self._max_duration)

        # while there can still be added connections do this
        while (line.duration + min(line.get_all_options().values(),
               key=lambda x: x[0].duration)[0].duration <= self._max_duration):

            # get random options from begin or end of this line
            options = rd.choice(line.get_begin_end_options())

            # add random connection from options to line
            connection_options = [option[0] for option in options.values()]
            line.add_connection(rd.choice(connection_options),
                                self._max_duration)

        return line

    def goal_function(self, lines, penalty=0):
        """
        define the goal function

        parameters:
            lines   - lines to calculate the goal function for;
            penalty - penalties for the lines (default is 0);

        returns the value of the goal function and the coverage
        """

        # predefine used connections and number of minutes to the penalty value
        used_connections = set()
        Min = penalty

        # for each line in lines find used connections and add minutes
        for line in lines:
            Min += line.duration
            for connection in line.connections:
                used_connections.add(connection)

        # calculate the coverage and define the number of lines
        p = len(used_connections)/len(self._connections)
        T = len(lines)

        return p * 10000 - (T * 100 + Min), p

    def run(self, repeat=1, progress_bar=True):
        """
        run this algorithm

        parameter:
            repeat          - number of repeats to do for this algorithm;
            progress_bar    - do I need to show the progress? (default True);

        returns the result
        """

        # make sure repeat is an interger
        try:
            int(repeat)
        except ValueError:
            exit("RunError: please make sure you've entered a int "
                 "for the number of repeats")

        # reset the result list and scores dict
        self._result = []
        self._scores = defaultdict(lambda: defaultdict(list))

        # show progress bar
        if progress_bar:

            # print running parameters
            print(f"Runing, Random {repeat} times")

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

                # create current number of lines
                for _ in range(n_of_l):
                    lines.append(self.create_line())

                # get score
                goal_function_result = self.goal_function(lines)

                # add result to results attribute and save score
                self._result.append((lines,) + goal_function_result)
                self._scores[n_of_l]["runs"].append(run)
                self._scores[n_of_l]["scores"].append(goal_function_result[0])

                # update progress bar
                if progress_bar:
                    step += 1

                    bar.update(step)

            # save the 5 best results
            self._result = sorted(self._result, key=lambda x: x[1],
                                  reverse=True)[:5]

        # finish the progress bar
        if progress_bar:
            bar.finish()

        return self._result
