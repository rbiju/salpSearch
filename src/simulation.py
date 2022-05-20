import pymunk

from creatures import Creature
from creature_chains import CreatureChain
from graphs import CreatureGraph
from handlers import CreaturePhysicsHandler, ConcentrationHandler, LinkHandler, RenderHandler


class Simulation:
    def __init__(self, creature_physics_handler: CreaturePhysicsHandler,
                 concentration_handler: ConcentrationHandler,
                 link_handler: LinkHandler,
                 creature_graph: CreatureGraph,
                 **kwargs):
        self.creature_physics_handler = creature_physics_handler
        self.concentration_handler = concentration_handler
        self.link_handler = link_handler
        self.creature_graph = creature_graph

        self.kwargs = kwargs

        self.creature_chain = self.create_chain()

        self.space = self.creature_physics_handler.space
        self.concentration_space = self.concentration_handler.concentration_space

        self.fps = 24
        self.dt = 1 / self.fps
        self.max_time = 15

    def create_chain(self):
        creature = Creature(self.creature_physics_handler, self.concentration_handler, **self.kwargs)

        return CreatureChain(creature=creature, creature_graph=self.creature_graph, link_handler=self.link_handler)

    def run(self):
        frame_counter = 0
        t = 0

        while t < self.max_time:
            t = self.dt * frame_counter
            self.creature_chain.run_chain()

            frame_counter += 1
            self.concentration_space.step(self.dt)
            self.space.step(self.dt)
