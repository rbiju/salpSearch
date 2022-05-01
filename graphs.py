from abc import ABC, abstractmethod

from typing import List


class CreatureGraph(ABC):
    def __init__(self, **kwargs):
        self.graph = None

    @abstractmethod
    def create_graph(self, num_creatures) -> List:
        raise NotImplementedError

    @abstractmethod
    def positions(self, starting_point, direction_vector) -> List[tuple]:
        raise NotImplementedError


class LinearChain(CreatureGraph):
    """Creates a graph and list of positions corresponding to a linear chain"""
    def __init__(self, *kwargs):
        super().__init__()
        self.num_creatures = kwargs['num_creatures']
        self.starting_point = kwargs['starting_point']
        self.direction_vector = kwargs['direction_vector']

    def create_graph(self, num_creatures) -> dict:
        graph = {0: [1]}
        for creature in range(1, num_creatures - 1):
            graph[creature] = [creature + 1, creature - 1]
        graph[num_creatures] = num_creatures - 1

        return graph


    def positions(self, starting_point: tuple, direction_vector: tuple) -> List[tuple]:
        pass
