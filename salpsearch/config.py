from dataclasses import dataclass
from typing import Tuple


# Spaces
@dataclass
class PhysicsSpaceConfig:
    space: str
    damping: float


@dataclass
class ConcentrationSpaceConfig:
    origin: Tuple[float, float]


# Physics and Concentration
@dataclass
class PhysicsHandlerConfig:
    space: PhysicsSpaceConfig
    type: str


@dataclass
class ConcentrationHandlerConfig:
    space: ConcentrationSpaceConfig
    type: str


# Creatures
@dataclass
class SalpConfig:
    physics_handler: PhysicsHandlerConfig
    concentration_handler: ConcentrationHandlerConfig
    pos: tuple
    radius: int
    thrust: int
    action_potential_baseline: float
    action_potential_step: float
    angle: int


# Links
@dataclass
class PinHandlerConfig:
    space: PhysicsSpaceConfig


@dataclass
class RotaryLimitHandlerConfig:
    space: PhysicsSpaceConfig
    min: float
    max: float


@dataclass
class DampedSpringConfig:
    space: PhysicsSpaceConfig
    stiffness: float
    damping: float


# Graphs
@dataclass
class LinearChainConfig:
    num_creatures: int
    starting_point: tuple
    direction_vector: tuple
    distance: int
