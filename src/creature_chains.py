from abc import ABC, abstractmethod
from copy import deepcopy
from typing import List
import math

from graphs import CreatureGraph
from creatures import Creature
from handlers import LinkHandler


class CreatureChain(ABC):
    def __init__(self):
        self.creature_list: List[Creature]
        pass

    @abstractmethod
    def make_chain(self):
        """Creates chain of creatures and links between them"""
        raise NotImplementedError

    @abstractmethod
    def run_chain(self):
        """Invokes jet propel method on all creatures in creature_list"""
        raise NotImplementedError

    @abstractmethod
    def get_center(self):
        """Returns physics position of center of chain"""
        raise NotImplementedError


class SalpChain(CreatureChain):
    def __init__(self, creature: Creature,
                 creature_graph: CreatureGraph,
                 link_handler: LinkHandler):
        super().__init__()
        self.creature = creature
        self.graph = creature_graph
        self.link_handler = link_handler
        self.creature_list = self.create_creature_list()
        self.make_chain()

    def create_creature_list(self) -> List[Creature]:
        creature_list = []
        for i in range(self.graph.num_creatures):
            pos = self.graph.positions[i]
            temp_creature = deepcopy(self.creature)
            temp_creature.pos = pos
            creature_list.append(temp_creature)
        return creature_list

    def make_chain(self):
        graph = self.graph.graph
        for key in graph:
            for val in graph[key]:
                self.link_handler.add_link(self.creature_list[key].body, self.creature_list[val].body)

    def run_chain(self):
        for creature in self.creature_list:
            creature.jet_decision()

    def get_center(self):
        if self.graph.num_creatures % 2 == 1:
            center_ndx = math.floor(self.graph.num_creatures / 2)
            return self.creature_list[center_ndx].pos
        else:
            center_ndx = self.graph.num_creatures / 2
            return (self.creature_list[center_ndx].pos + self.creature_list[center_ndx - 1].pos) / 2.0
