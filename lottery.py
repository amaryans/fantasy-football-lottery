import numpy as np
import pandas as pd

from lottery_simulator import Simulator

class LotterySim():
    def __init__(self):
        self.n_picks = 12
        self.n_balls = 4
        self.places = ['TCoop', 'Dom', 'Carson', 'Gus', 'Logan', 'Beans', 'Sam', 'Austin', 'Addi', 'Jakeb', 'Batches', 'Owen']
        self.chances = [200, 175, 150, 120, 90, 75, 60, 45, 37, 28, 18, 7]
        self.sim = Simulator(self.n_picks, self.n_balls, self.chances)

    def runSampleSim(self):
        iters = 10000
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