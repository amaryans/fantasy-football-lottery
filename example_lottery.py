import numpy as np
import pandas as pd

from lottery_simulator import Simulator

class LotterySim():
    def __init__(self):
        self.n_picks = 12
        self.n_balls = 4
        self.places = ['TCoop', 'Dom', 'Carson', 'Gus', 'Logan', 'Beans', 'Sam', 'Austin', 'Addi', 'Jakeb', 'Batches', 'Owen']
        self.chances = [200, 175, 150, 120, 90, 75, 60, 45, 37, 28, 18, 7]
        self.sim = Simulator(n_picks, n_balls, self.chances)

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
        lottery_simulation = np.array([sim.play_lottery() for _ in range(iters)])
        print(lottery_simulation)

# n_picks = 12
# n_balls = 4
# places = ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', '10th', '11th', '12th']
# chances = [200, 175, 150, 120, 90, 75, 60, 45, 37, 28, 18, 7]


# sim = Simulator(n_picks, n_balls, chances)
# iters = 10000
# lottery_simulation = np.array([sim.play_lottery() for _ in range(iters)])


# df = pd.DataFrame({'seeds': np.array(sim.seeds) + 1, 'chances': chances}).set_index('seeds')

# for i in range(len(places)):
#     df[places[i]] = (np.round(np.bincount(lottery_simulation[:, i], minlength=len(places)) / len(lottery_simulation), 3))
# df.to_csv('./example_result/conditional_probabilities.csv')

# # Start of the UI

# sim = Simulator(n_picks, n_balls, chances)
# iters = 1
# lottery_simulation = np.array([sim.play_lottery() for _ in range(iters)])

# #print("lol")
# # Carson, Coop, Beans, Gus, Owen, Addi, Jakeb, Sam, Austin, Batches, Logan, Dom
# places = ['Dom', 'Logan', 'Batches', 'Austin', 'Sam', 'Jakeb', 'Addi', 'Owen', 'Gus', 'Beans', 'TCoop', 'Carson']
# places = ['Dom', 'Logan', 'Batches', 'Austin', 'Sam', 'Jakeb', 'Addi', 'Owen', 'Gus', 'Beans', 'TCoop', 'Carson']
# df = pd.DataFrame({'seeds': np.array(sim.seeds) + 1, 'chances': chances}).set_index('seeds')

# for i in range(len(places)):
#     df[places[i]] = (np.round(np.bincount(lottery_simulation[:, i], minlength=len(places)) / len(lottery_simulation), 3))

# pick = ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', '10th', '11th', '12th']
# places = ['Dom', 'Logan', 'Batches', 'Austin', 'Sam', 'Jakeb', 'Addi', 'Owen', 'Gus', 'Beans', 'TCoop', 'Carson']
# #print(len(places))
# order = ['','','','','','','','','','','','']
# iter = 0
# for place in places:
#     #print(place)
#     #print(df[place].values)
#     iter_1 = 0
#     for i in (df[place].values):
#         #print(i)
#         if i:
#             order[iter] = places[iter_1]
#             iter = iter+1
#         iter_1 = iter_1 + 1

# #print(order)



# print("#################################################################")
# print("### Welcome to the West K-Town Fantasy Football Draft Lottery ###")
# print("#################################################################")
# print("\n")

# draft_order = ['','','','','','','','','','','','']

# for team in order:
#     print(team, "may now select their pick")
#     print("Where would you like to select in this year's draft?")
#     while True:
#         try:
#             draft_spot = int(input())
#         except:
#             print("Not a valid value")
#             continue
        
#         if draft_spot > 12:
#             print("Not a valid draft spot")
#             continue
#         elif draft_order[draft_spot - 1] != '':
#             print("This spot has already been taken by", draft_order[draft_spot - 1])
#             continue
#         else:
#             draft_order[draft_spot - 1] = team
#             print(team, "is selecting in spot number", draft_spot)
#             print("\n")
#             print("CURRENT DRAFT ORDER:")
#             print(draft_order)
#             print("\n")
#             break



# print("The final draft order for this year's draft is:\n")
# i = 0
# places = ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', '10th', '11th', '12th']
# for team in draft_order:
#     print(places[i])
#     print(team,"\n")
#     i += 1




