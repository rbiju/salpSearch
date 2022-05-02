from abc import ABC, abstractmethod
from handlers import PhysicsHandler, ConcentrationHandler
from graphs import CreatureGraph


class CreatureChain(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def make_chain(self):
        raise NotImplementedError


class SalpChain():
    def __init__(self, physics_handler: PhysicsHandler,
                 concentration_handler: ConcentrationHandler,
                 creature_graph: CreatureGraph):
        self.physics_handler = physics_handler
        self.concentration_handler = concentration_handler
        self.graph = creature_graph

    def make_chain(self):
        pass
