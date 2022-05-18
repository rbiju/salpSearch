import pymunk

from creatures import Creature
from creature_chains import CreatureChain
from handlers import CreaturePhysicsHandler, ConcentrationHandler, LinkHandler, RenderHandler


class Simulation():
    def __init__(self, creature: Creature, creature_chain: CreatureChain):
        self.creature = creature
        self.creature_chain = creature_chain
        self.space = pymunk.Space()

        self.fps = 24
        self.dt = 1 / self.fps
        self.max_time = 15

    def run(self, point_of_interest):
        frame_counter = 0
        t = 0

        while t < self.max_time:
            t = self.dt * frame_counter
            self.creature_chain.run_chain()
            frame_counter += 1

            self.space.step(self.dt)