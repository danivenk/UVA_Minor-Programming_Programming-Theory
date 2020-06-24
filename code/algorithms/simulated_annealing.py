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

from code.algorithms import Hill_Climber


class Simulated_Annealing(Hill_Climber):
    """
    Defines the Simulated_Annealing algorithm
        has inheritance from Hill_Climber

    parameters:
        connections     - connections in database;
        max_duration    - maximal duration for a line
        max_n_of_l      - maximal number of lines;

    methods:
        temperature         - temperature for this iteration;
        acceptation_chance  - calc accept chance from score diff and temp;
        run                 - runs algorithm for specified values;
    """

    def __init__(self, connections, max_duration, max_n_of_l):
        """
        Initializes the Simulated Annealing Algorithm

        parameters:
            connections     - connections in database;
            max_duration    - maximal duration for a line
            max_n_of_l      - maximal number of lines;
        """

        # init Simulated Annealing from inheritance
        super().__init__(connections, max_duration, max_n_of_l)

    def temperature(self, startT, iteration):
        """
        temperature for this iteration

        parameters:
            startT      - starting temperature;
            iteration   - current iteration;

        returns the temperature
        """

        return startT * .997 ** iteration

    def acceptation_chance(self, old_score, new_score, temperature):
        """
        calc accept chance from score diff and temp

        parameters:
            old_score   - previous score
            new_score   - possible next score
            temperature - current temperature
        """

        return 2**((old_score - new_score)/temperature)

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

        # reset the result list and scores dict
        self._result = []
        self._scores = defaultdict(lambda: defaultdict(list))

        # print running paramters
        print(f"Runing, Simulated Annealing {repeat} times with "
              f"{iterations} iterations per run")

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

                # starting temperature, to be decided
                startT = iterations

                # get the current chance
                chance = self.acceptation_chance(self._current_state[1],
                                                 score[0],
                                                 self.temperature(startT,
                                                                  iteration))

                # accept if score is higher than old score or chance is right
                if score[0] > self._current_state[1] or rd.random() < chance:
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
