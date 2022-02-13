import numpy as np
import salpSim as salp
from importlib import reload

reload(salp)

# genetic algorithm to optimize salp simulation hyperparameters
""" params to optimize:
salp number -
threshold constant -
default threshold -
thrust - 
distance
number of salps -
"""

# salp.App(FPS, salpNum, thresholdConst, defaultThresh, thrust, distance)
sampleRun = salp.App(15, 3, 0.0004, 0.002, 1000, 10)
sampleRun.run()
print(sampleRun.fitness)


def gen_mutants(salp: salp.App, volatility: float, num_mutants: int) -> list:
    mutant_list = []
    for i in range(0, num_mutants):
        mutant_list[i] = salp.App(15, np.random.randint(3, 11, 2), np.random.rand)


def run_sim(salpList: list):


def
