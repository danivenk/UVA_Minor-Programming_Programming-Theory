#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
version: python 3.8
arg_class.py defines the Arg class for the input of the command line
Dani van Enk, 11823526
"""


class Arg():
    """
    the Arg class defines an argument option in the commandline

    parameters:
        aliases         - all aliases for this argument;
        description     - description of this argument;
        optional        - is this argument optional (default False);
        argument_type   - argument type (default str);

    properties:
        aliases         - returns the aliases of this argument;
        description     - returns the description of this argument;
        argument_type   - returns the argument_type of this argument;
        value           - returns the value of this argument;
            setter sets value and converts to argument_type;
        optional        - returns if this argument is optional;
        name            - returns the name of the argument;
    """

    def __init__(self, aliases, description, optional=False,
                 argument_type="str"):
        """
        initializes an argument

        parameters:
            aliases         - all aliases for this argument;
            description     - description of this argument;
            optional        - is this argument optional (default False);
            argument_type   - argument type (default str);
        """

        self._aliases = aliases
        self._description = description
        self._argument_type = argument_type
        self._value = None
        self._optional = optional

    @property
    def aliases(self):
        """
        returns the aliases of this argument
        """

        return self._aliases

    @property
    def description(self):
        """
        returns the description of this argument
        """

        return self._description

    @property
    def argument_type(self):
        """
        returns the argument_type of this argument
        """

        return self._argument_type

    @property
    def value(self):
        """
        returns the value of this argument
        """

        return self._value

    @value.setter
    def value(self, value):
        """
        sets the value and converts it to it's correct type
        """

        # if argument is of type int make sure value becomes int
        if self._argument_type == "int":
            try:
                self._value = int(value)
            except ValueError:
                exit("value is not a integer")
        # else keep it as the value given
        else:
            self._value = value

    @property
    def optional(self):
        """
        returns if this argument is optional
        """

        return self._optional

    @property
    def name(self):
        """
        returns the name of the argument
        """

        # set name to value of '--' alias
        for alias in self._aliases:
            if "--" in alias:
                return alias.lstrip("--")

        # set name to value of '-' alias
        for alias in self._aliases:
            if "-" in alias:
                return alias.lstrip("-")

        # set name to alias
        return alias

    def __str__(self):
        """
        set string to print when object is being printed
        """

        return f'{", ".join(self._aliases):<20} {self.description}'
