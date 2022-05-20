from abc import ABC, abstractmethod
from typing import Dict

from math import radians
import numpy as np
import pymunk
from pymunk.vec2d import Vec2d

from handlers import CreaturePhysicsHandler, ConcentrationHandler


# space = pymunk.Space()
# space.damping = 0.8
# disp = 800


class Creature(ABC):
    """Abstract class representing various creature types
    Creatures should:
        - measure concentration
        - be aware of their position
        - propel self within simulation
    """
    def __init__(self, physics_handler: CreaturePhysicsHandler,
                 concentration_handler: ConcentrationHandler,
                 **kwargs: Dict[str: any]):
        self.physics_handler = physics_handler
        self.concentration_handler = concentration_handler
        self.body = None
        self.pos: pymunk.vec2d
        pass

    @property
    @abstractmethod
    def pos(self):
        return self.body.position

    @pos.setter
    @abstractmethod
    def pos(self, pos):
        self.pos = pos

    @abstractmethod
    def get_conc(self):
        raise NotImplementedError

    @abstractmethod
    def jet_propel(self, thrustVec):
        raise NotImplementedError

    @abstractmethod
    def jet_decision(self):
        raise NotImplementedError


class Salp(Creature):
    """
    Depends on PhysicsHandler and ConcentrationHandler abstractions.
    Salps can:
        - measure concentration at their current location
        - modulate an internal action potential based on measured concentration
        - propel self by applying impulse through center of mass

    kwargs:
        radius: int
            Radius of salp (modeled as a circle for simplicity
        angle: int
            Starting angle of salp, will be used as thrust direction
        thrust: int
            Value of thrust to apply (1000 works well)
        action_potential_baseline: float
            Value of ap after firing (drop to 'zero')
        action_potential_step: float
            Amount to increase AP voltage given zero concentration at salp's location (decreases as concentration rises)
    """

    def __init__(self, pos,
                 physics_handler: CreaturePhysicsHandler, concentration_handler: ConcentrationHandler,
                 **kwargs):
        super().__init__(physics_handler, concentration_handler, **kwargs)
        self.physics_handler = physics_handler
        self.concentration_handler = concentration_handler
        self.pos = pos
        self.radius = kwargs['radius']
        self.body = self.physics_handler.create_body(self.radius, self.pos)
        self.body.angle = radians(kwargs['angle'])
        self.thrust = kwargs['thrust']

        # action potential properties
        self.action_potential_baseline = kwargs['action_potential_baseline']
        self.action_potential_step = kwargs['action_potential_step']
        self.voltage = self.action_potential_baseline

        self.physics_handler.add_body(self.body)

    @property
    def pos(self):
        return self.body.position

    @pos.setter
    def pos(self, pos):
        self.pos = pos

    def get_conc(self) -> float:
        return self.concentration_handler.get_conc(self.pos)

    # TODO unit test
    def jet_propel(self, thrustVec: Vec2d) -> bool:
        seed = np.random.rand()
        if seed < self.voltage:
            self.body.apply_impulse_at_local_point(thrustVec * self.thrust, (0, 0))
            return True
        else:
            return False

    # TODO unit test
    def threshold_update(self):
        salpConc = self.get_conc() / 255
        ap_step = self.action_potential_step * (1 - np.tanh(salpConc))
        return ap_step

    # TODO unit test
    def jet_decision(self):
        thrust_vec = Vec2d(0, 1) * self.body.angle
        if self.jet_propel(thrust_vec):
            self.voltage = self.action_potential_baseline
        elif not self.jet_propel(thrust_vec):
            self.voltage += self.threshold_update()
