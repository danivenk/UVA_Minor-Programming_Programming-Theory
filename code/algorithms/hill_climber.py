"""
version: python 3.8
hill_climber.py defines the Hill Climbing algorithm

authors:
    Dani van Enk, 11823526
    Michael Faber, 6087582
"""


# used imports
import random as rd
import copy
import progressbar as pbar

from collections import defaultdict

from code.algorithms import Random_Connections, A_Star
from code.classes import Line


class Hill_Climber(Random_Connections):
    """
    Defines the Hill Climber algorithm
        has inheritance from Random_Connections

    parameters:
        connections     - connections in database;
        max_duration    - maximal duration for a line
        max_n_of_l      - maximal number of lines;

    methods:
        get_available_connections   - finds all available/not used connections;
        find_dupes_and_index        - finds all duplicate connections of line;
        chang_section               - change a section of a line;
        ends_cut                    - cuts end of random line in lines;
        remove_duplicates           - remove a duplicate connection from line;
        add_missing                 - adds missing connections where possible;
        change_line_section         - change a random line section;
        run                         - runs algorithm for specified values;
    """

    def __init__(self, connections, max_duration, max_n_of_l):
        """
        Initializes the Hill Climber Algorithm

        parameters:
            connections     - connections in database;
            max_duration    - maximal duration for a line
            max_n_of_l      - maximal number of lines;
        """

        # init Hill Climber from inheritance
        super().__init__(connections, max_duration, max_n_of_l)

        # get state from running inheritance
        self._current_state = super().run(progress_bar=False)[0]

        # define path_finder object
        self._pathfinder = A_Star(connections, max_duration)

    def get_available_connections(self, lines):
        """
        gets available connections

        parameter:
            lines - contains the used connections;

        returns available connections
        """

        # predefining used connections dictionary
        used_connections = dict()

        # loop over all lines and add used connections
        for line in lines:
            for connection in line.connections:
                used_connections[str(connection)] = connection

        # define all connections dictionary
        all_connections = {str(connection): connection
                           for connection in self._connections}

        # find the difference between all connections and used connections
        available_connections = \
            [all_connections[connection] for connection in
                all_connections.keys() - used_connections.keys()]

        return available_connections

    def find_dupes_and_index(self, line):
        """
        find duplicate connections in line and their indices

        parameter:
            line - line to find duplicates in

        returns line back, None if no dupes found
        """

        # make sure line is of type Line
        try:
            assert type(line) is Line
        except AssertionError:
            exit("make sure line is of type Line")

        # make empty dupe list
        dupes = []

        # preset counter, current_connection and indices
        current_count = 1
        cur_conn = None
        i = 0
        begin, end = (0, 0)

        # loop over the connections in the line
        for i, connection in enumerate(line.connections):

            # at the start define connection
            if not cur_conn and current_count == 1:
                cur_conn = connection
                begin = i

            # if connection has been found again add counter
            elif cur_conn == connection:
                current_count += 1

            # if different connection, add values to dupes list, reset values
            else:
                end = i - 1

                # only add if more than 1 connection has been found
                if current_count > 1:
                    dupes.append((cur_conn, current_count, begin, end))

                cur_conn = connection
                current_count = 1
                begin = i

        # make sure the last one is added
        if end != i:
            end = i

            # only add if more than 1 connection has been found
            if current_count > 1:
                dupes.append((cur_conn, current_count, begin, end))

        # if dupes has been found return them else None
        if len(dupes) >= 1:
            return dupes
        else:
            return None

    def change_section(self, line, random=True, **kwargs):
        """
        change a section of the line, can be random or specific

        parameters:
            line        - line to be changed;
            random      - change random section? (default True);
            kwargs      - can contain index0, index1 as start and end of
                            the to be changed section;

        returns the changed line
        """

        # predefine index0 and index1 as 0
        index0, index1 = 0, 0

        # if a random section is to be changed choose random indices
        if random:

            # make sure the indices can define a section
            while (index0 == index1 or index0 > index1):
                index0 = rd.randint(0, len(line.stations) - 1)
                index1 = rd.randint(index0, len(line.stations) - 1)

        # if not random and index0 and index1 are given check if valid
        elif "index0" in kwargs.keys() and "index1" in kwargs.keys():
            index0 = kwargs["index0"]
            index1 = kwargs["index1"] + 1

            # if index0 and index1 can't define a section exit
            if index0 == index1 or index0 > index1:
                exit("make sure index0 is not equal to/smaller than index1 "
                     "and in kwargs")
        else:
            exit("if you choose not random make "
                 "sure index0 and index1 are defined")

        # define ends (stations) of the section
        station1 = line.stations[index0]
        station2 = line.stations[index1]

        # split the line at index0 and index1 (station indices)
        line0, line1 = line.split_line(index0, self._max_duration)
        line1, line2 = line1.split_line(index1 - index0, self._max_duration)

        # find a different path for this section (shortest by default)
        line1 = self._pathfinder.create_line(station1, station2)

        # make list with all line segments and start new line object
        line_segments = [line0, line1, line2]
        line = Line(line0.begin_end_station[0])

        # rebuilt the line from it's line segments
        for line_ in line_segments:
            for connection in line_.connections:
                line.add_connection(connection, self._max_duration)

        return line

    def ends_cut(self, lines):
        """
        cuts the ends from random line at random end

        parameter:
            lines - lines to change;

        returns None if failed, state if successful
        """

        if len(lines) <= 1:
            None

        # get random line
        line = rd.choice(lines)

        # get line connections
        connections = line.connections

        # get random end of line
        current_HEAD_index, direction = \
            rd.choice(line.begin_end_station_index)

        # make sure line has more than one connection
        if len(connections) <= 1:
            return None

        # check if duplicate connections present at the chosen end
        if connections[current_HEAD_index] == \
                connections[current_HEAD_index + direction]:

            # remove duplicate connection
            line.stations.pop(current_HEAD_index)
            line.connections.pop(current_HEAD_index)

            return lines

        return None

    def remove_duplicates(self, lines):
        """
        remove duplicate connections (dupes) in random line from lines

        parameter:
            lines - lines to choose line from to remove dupes from;

        returns lines back or None if failed
        """

        if len(lines) <= 1:
            None

        # choose random line_index from lines
        line_index = rd.randint(0, len(lines) - 1)

        # remove line from lines
        line = lines.pop(line_index)

        # find the dupes
        dupes = self.find_dupes_and_index(line)

        # if dupes found choose random dupe else return None
        if dupes:
            remove_duplicate = rd.choice(dupes)
        else:
            return None

        # find the minimum number of connections needed for this section
        line = self.change_section(line, random=False,
                                   index0=remove_duplicate[2],
                                   index1=remove_duplicate[3])

        # insert line back into lines
        lines.insert(line_index, line)

        return lines

    def add_missing(self, lines):
        """
        add missing connections to state where possible

        parameter:
            lines - lines to choose random line to change from;

        returns None if failed, lines if successful
        """

        if len(lines) <= 1:
            None

        # define empty used_connections set
        used_connections = set()

        # get all used connections
        for line in lines:
            used_connections.update(line.connections)

        # find coverage (p)
        p = len(used_connections)/len(self._connections)

        # get duration condition for each line, duration < max duration
        duration_condition = \
            [line.duration < self._max_duration for line in lines]

        # if there are connections missing
        #   duration condition can be satisfied
        if p < 1 and any(duration_condition):

            # get available connections
            available_connections = self.get_available_connections(lines)

            # choose random line
            line = rd.choice(lines)

            # choose random missing connection
            connection = rd.choice(available_connections)

            # define missing_path empty list
            missing_path = []

            # loop for station at the ends of the line
            for station1 in line.begin_end_station:

                # loop for station at the end of a connection
                for station2 in connection.section:

                    # look for path between connection and line end
                    #   if not next to each other
                    if station1 != station2:
                        path = self._pathfinder.create_line(station1, station2)
                        missing_path.append(path)

            # find the shortest path found
            path = min(missing_path, key=lambda x: x.duration)

            # add connection to path if not already present
            if connection not in path.connections:
                path.add_connection(connection, self._max_duration)

            # make sure path can be added because of duration
            if line.duration + path.duration > self._max_duration:
                return None

            # add path to line
            for path_connection in path.connections:
                if path_connection in line.connections and \
                        line.stations[-1] != path.stations[0]:
                    pass
                elif not line.add_connection(path_connection,
                                             self._max_duration):
                    return None

            return lines

        return None

    def change_line_section(self, lines):
        """
        change random line section of random line from lines

        parameter:
            lines - list of lines to choose line from;

        returns back lines
        """

        if len(lines) <= 1:
            None

        # choose random line_index
        line_index = rd.randint(0, len(lines) - 1)

        # remove line from lines
        line = lines.pop(line_index)

        # change random line_section of line
        line = self.change_section(line)

        # insert line back into lines
        lines.insert(line_index, line)

        return lines

    def run(self, repeat=1, iterations=1):
        """
        run this algorithm

        parameters:
            repeat      - number of times to repeat the algorithm (default 1);
            iterations  - number of tries to change the current state
                (default 1);
        """

        # make sure iterations and repeat are integers
        try:
            int(repeat)
            int(iterations)
        except ValueError:
            exit("RunError: please make sure you've entered a integer "
                 "for the number of repeats and iterations")

        # print running paramters
        print(f"Runing, Hill Climber {repeat} times with "
              f"{iterations} iterations per run")

        # reset the result list and scores dict
        self._result = []
        self._scores = defaultdict(lambda: defaultdict(list))

        # define the progressbar widgets
        bar_widgets = [pbar.Bar("#", "[", "]"), " ", pbar.ETA()]

        # define the progress bar and start it
        bar = pbar.ProgressBar(maxval=repeat*iterations,
                               widgets=bar_widgets).start()

        # repeat the algorithm as many times as specified
        for run in range(repeat):
            # loop for each iteration
            for iteration in range(iterations):

                # create a copy of the current state
                state = copy.deepcopy(self._current_state)

                # define options
                options = [self.ends_cut, self.add_missing,
                           self.remove_duplicates, self.change_line_section]

                # define lines (from state)
                lines = state[0]

                # choose random option
                new_lines = rd.choice(options)(lines)

                # make sure option worked
                if new_lines:
                    lines = new_lines

                # get new score
                score = self.goal_function(lines)

                # check if score has been improved
                if score[0] > self._current_state[1]:
                    self._current_state = (lines,) + score

                # add result to results attribute and save score/iterations
                self._result.append(self._current_state)
                self._scores[run]["iterations"].append(iteration)
                self._scores[run]["scores"].append(self._current_state[1])

                # save the 5 best results
                self._result = sorted(self._result, key=lambda x: x[1],
                                      reverse=True)[:5]

                # update progress bar
                bar.update(run*iterations + iteration + 1)

        # finish progress bar
        bar.finish()

        return self._result
