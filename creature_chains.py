from abc import ABC, abstractmethod
from copy import deepcopy

from handlers import PhysicsHandler, ConcentrationHandler
from graphs import CreatureGraph
from creatures import Creature, Salp


class CreatureChain(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def make_chain(self):
        raise NotImplementedError


class SalpChain():
    def __init__(self, creature: Creature,
                 creature_graph: CreatureGraph,
                 **kwargs):
        self.creature = creature
        self.graph = creature_graph

    def create_creature_list(self):
        creature_list = []
        for i in range(self.graph.num_creatures):
            pos = self.graph.positions[i]
            temp_creature = deepcopy(self.creature)
            temp_creature.pos = pos
            creature_list.append(temp_creature)
