from abc import ABC, abstractmethod
from pymunk.vec2d import Vec2d
from typing import List


class CreatureGraph(ABC):
    def __init__(self, **kwargs):
        self.graph = None

    # TODO unit test
    @staticmethod
    def deduplicate_graph(graph: dict):
        deduplicated_graph = {}
        for key in graph:
            deduplicated_graph[key] = [val for val in graph[key] if val not in deduplicated_graph]

        return deduplicated_graph

    @abstractmethod
    def graph(self) -> List:
        raise NotImplementedError

    @abstractmethod
    def positions(self) -> List[tuple]:
        raise NotImplementedError


class LinearChain(CreatureGraph):
    """Creates a graph and list of positions corresponding to a linear chain
    kwargs:
        num_creatures: int
            number of sslps to include in chain
        starting_point: tuple (converted to Vec2D)
            refers to the position of the center of the chain
        direction_vector: tuple (converted to Vec2D)
            points in a direction orthogonal to the chain, aligned with the direction of thrust
        distance: float
            distance between salps (must be larger than salp diameter)

    properties:
        graph: dict
            representation of creature connections. deduplicated.
        positions: List[tuple]
            list of salp positions where index corresponds with index stored in graph"""

    def __init__(self, **kwargs):
        super().__init__()
        self.num_creatures = kwargs['num_creatures']
        self.starting_point = Vec2d(kwargs['starting_point'])
        self.direction_vector = Vec2d(*kwargs['direction_vector']).normalized()
        self.distance = kwargs['distance']

    # TODO unit test
    @property
    def graph(self) -> dict:
        graph = {0: [1]}
        for creature_ndx in range(1, self.num_creatures - 1):
            graph[creature_ndx] = [creature_ndx + 1, creature_ndx - 1]
        graph[self.num_creatures] = self.num_creatures - 1

        return self.deduplicate_graph(graph)

    # TODO unit test
    @property
    def positions(self) -> List[tuple]:
        """List of salp positions"""
        chain_length = self.num_creatures * self.distance
        chain_vector = self.direction_vector.perpendicular_normal()  # rotates by +90 degrees
        first_position = self.starting_point - (chain_length * 0.5 * chain_vector)
        positions = []
        for i in range(0, self.num_creatures):
            positions.append(first_position + (i * self.distance * chain_vector))

        return positions
