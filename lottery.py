import numpy as np
import pandas as pd

from lottery_simulator import Simulator
from config.config_manager import config

class LotterySim():
    def __init__(self):
        # Load configuration from config manager
        self.n_picks = config.number_of_teams
        self.n_balls = 4
        self.places = config.owner_names
        self.places.reverse()
        # Generate chances based on standings (reverse order - worst team gets most chances)
        # This creates a decreasing sequence of chances
        if len(self.places) > 0:
            max_chance = 200
            min_chance = 7
            step = (max_chance - min_chance) / (len(self.places) - 1) if len(self.places) > 1 else 0
            self.chances = [int(max_chance - i * step) for i in range(len(self.places))]
        else:
            self.chances = []

        self.sim = Simulator(self.n_picks, self.n_balls, self.chances)

    def runSampleSim(self):
        iters = 100
        lottery_simulation = np.array([self.sim.play_lottery() for _ in range(iters)])
        df = pd.DataFrame({'seeds': np.array(self.sim.seeds) + 1, 'chances': self.chances}).set_index('seeds')

        for i in range(len(self.places)):
            print(self.places[i])
            df[self.places[i]] = (np.round(np.bincount(lottery_simulation[:, i], minlength=len(self.places)) / len(lottery_simulation), 3))
        df.to_csv('./example_result/conditional_probabilities.csv')

    def runSim(self):
        iters = 1
        lottery_simulation = np.array([self.sim.play_lottery() for _ in range(iters)])

        pickOrder = []
        for i in range(len(lottery_simulation[0])):
            pickOrder.append(self.places[lottery_simulation[0][i]])
        return pickOrder