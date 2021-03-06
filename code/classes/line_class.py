"""
version: python 3.8
line_class.py defines the Line classe used for the database

authors:
    Dani van Enk, 11823526
    Michael Faber, 6087582
"""

# import used classes
import code.classes as clss


class Line():
    """
    the Line class defines a combination of connections
        (and thus also stations)

    parameters:
        id              - is the lineid;
        connections     - all connections present in this line;
        stations        - the stations of this line in the correct order;

    properties:
        duration                    - returns duration of this line;
        no_of_stations              - returns number of station in this line;
        stations                    - returns stations list of this line;
        connections                 - returns connections list of this line;
        penalty                     - returns the penalty value of this line;
        begin_end_station           - returns the begin and end stations;
        begin_end_station_index     - returns the begin end indices;

    method:
        add_to_penalty          - add value to penalty;
        get_begin_end_options   - get begin and end options for this line;
        get_all_options         - get all options for this line;
        add_connection          - adds connection to line if valid;
            true if added correctly false if not;
        split_line              - splits the line into 2 lines at given index;
    """

    # define general unique identifier
    guid = 0

    def __init__(self, init_station=None):
        """
        initialize the Line class

        parameter:
            id              - Line-ID;
            init_station    - specific starting station;
        """

        try:
            assert type(init_station) is clss.Station or not init_station
        except (ValueError, AssertionError):
            exit("make sure init_station is of type Station")

        self._id = self.guid
        self._connections = []
        self._penalty = 0

        # increase general unique identifier
        Line.guid += 1

        # if initial station defined start stations list with that station
        if init_station:
            self._stations = [init_station]
        else:
            self._stations = []

    @property
    def duration(self):
        """
        returns the duration of this line
        """

        # predefine the duration to 0
        _duration = 0

        # loop over all the connections of this line and add to the duration
        for connection in self._connections:
            _duration += connection.duration

        # make sure the duration is 0 or more
        if _duration < 0:
            raise ValueError(f"{_duration} is smaller than 0")
        else:
            return _duration

    @property
    def no_of_stations(self):
        """
        return the number of stations of this line
        """

        return len(self._stations)

    @property
    def stations(self):
        """
        return the stations list
        """

        return self._stations

    @property
    def connections(self):
        """
        return the connections list
        """

        return self._connections

    @property
    def penalty(self):
        """
        return penalty value
        """

        return self._penalty

    @penalty.setter
    def penalty(self, value):
        """
        set penalty value
        """

        # make sure value is a number
        try:
            float(value)
        except ValueError:
            exit("AdditionError: make sure value is a number")

        self._penalty = value

    def add_to_penalty(self, value):
        """
        add to penalty value
        """

        # make sure value is a number
        try:
            float(value)
        except ValueError:
            exit("AdditionError: make sure value is a number")

        self._penalty += value

    @property
    def begin_end_station(self):
        """
        return the begin and end stations
        """

        return [self._stations[0], self._stations[-1]]

    @property
    def begin_end_station_index(self):
        """
        returns the begin end indices and direction to go to
        """

        return (0, 1), (-1, -1)

    def get_begin_end_options(self):
        """
        get begin and end options for this line separately

        returns begin and end options
        """

        # if no stations are present return None
        if len(self._stations) == 0:
            return None

        # define the stations at the end of the current line
        self._current_start = self._stations[0]
        self._current_end = self._stations[-1]

        return self._current_start.connections, self._current_end.connections

    def get_all_options(self):
        """
        get all options for this line

        returns all options
        """

        # if no stations are present return None
        if len(self._stations) == 0:
            return None

        # define the stations at the end of the current line
        self._current_start = self._stations[0]
        self._current_end = self._stations[-1]

        # add to connections the begin and end options
        connections = self._current_start.connections.copy()
        connections.update(self._current_end.connections)

        return connections

    def add_connection(self, connection, max_duration):
        """
        adds a connection to the connections list if the connection is valid

        parameters:
            connection          - connection to be added;
            max_duration        - max duration of this line;

        returns True if the connection was successfully added and false if not
        """

        # check if connection is type Conenction and max_duration is a number
        try:
            assert type(connection) is clss.Connection
            max_duration = float(max_duration)
        except (AssertionError, ValueError):
            exit("LineAddConnectionError: please make sure the connection "
                 "you're adding is a connection object\n "
                 "and max_duration is a number")

        # check if the connection to be added makes the duration more than max
        if self.duration + connection.duration > max_duration:
            return False
        else:

            # if line is empty add whole connection
            if len(self._stations) == 0:

                for station in connection.section:
                    self._stations.append(station)

                self._connections.append(connection)

            # if not add it where it's posisble
            else:
                # get options
                current_start_options, current_end_options = \
                    self.get_begin_end_options()

                # if connection fits at the end add to the end
                if connection.cid in current_end_options:
                    next_station = current_end_options[connection.cid][1]
                    self._stations.append(next_station)
                    self._connections.append(connection)

                # if connection fits at the begin add to the begin
                elif connection.cid in current_start_options:
                    previous_station = current_start_options[connection.cid][1]
                    self._stations.insert(0, previous_station)
                    self._connections.insert(0, connection)
                else:
                    return False

        return True

    def split_line(self, index, max_duration):
        """
        splits line into 2 at given index

        parameters:
            index           - index to split the line at;
            max_duration    - maximum duration of a line;
        """

        # create 2 lines one starting at the start of the line
        line1 = Line(self.begin_end_station[0])
        line2 = Line()

        # loop over each connection
        for i, connection in enumerate(self.connections):
            # split it over the 2 lines
            if i < index:
                line1.add_connection(connection, max_duration)
            elif i >= index:
                line2.add_connection(connection, max_duration)

        return line1, line2

    def __repr__(self):
        """
        return representation of this class
        """

        return f"ID {self._id}"
