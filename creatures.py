from abc import ABC, abstractmethod

from math import radians
import numpy as np
from pymunk.vec2d import Vec2d

from handlers import PhysicsHandler, ConcentrationHandler


# space = pymunk.Space()
# space.damping = 0.8
# disp = 800


class Creature(ABC):
    def __init__(self, physics_handler, concentration_handler, **kwargs):
        self.physics_handler = physics_handler
        self.concentration_handler = concentration_handler
        pass

    @abstractmethod
    def get_conc(self):
        raise NotImplementedError

    @abstractmethod
    def jet_propel(self, thrustVec):
        raise NotImplementedError


class Salp(Creature):
    """
    Depends on PhysicsHandler and ConcentrationHandler abstractions.
    Salps can:
    1. measure the concentration at their current location
    2. modulate an internal action potential based on measured concentration
    3. propel self by applying impulse through center of mass

    kwargs:
        Radius: Radius of salp (modeled as a circle for simplicity
        Angle: Starting angle of salp, will be used as thrust direction
        Thrust: Value of thrust to apply (1000 works well)
        Action_potential_baseline: Value of ap after firing (drop to 'zero')
        Action_potential_step: Amount to increase AP voltage given zero concentration at salp's location
        -- (decreases as concentration rises)
    """
    def __init__(self, pos,
                 physics_handler: PhysicsHandler, concentration_handler: ConcentrationHandler,
                 **kwargs):
        super().__init__(physics_handler, concentration_handler, **kwargs)
        self.physics_handler = physics_handler
        self.concentration_handler = concentration_handler
        self.radius = kwargs['radius']
        self.body = self.physics_handler.create_body(self.radius, pos)
        self.body.angle = radians(kwargs['angle'])
        self.thrust = kwargs['thrust']

        # action potential properties
        self.action_potential_baseline = kwargs['action_potential_baseline']
        self.action_potential_step = kwargs['action_potential_step']
        self.voltage = self.action_potential_baseline

    def get_conc(self) -> float:
        return self.concentration_handler.get_conc(self.body.position)

    def jet_propel(self, thrustVec: Vec2d) -> bool:
        seed = np.random.rand()
        if seed < self.voltage:
            self.body.apply_impulse_at_local_point(thrustVec * self.thrust, (0, 0))
            return True
        else:
            return False

    def threshold_update(self):
        salpConc = self.get_conc() / 255
        ap_step = self.action_potential_step * (1 - np.tanh(salpConc))
        return ap_step

    def jet_decision(self):
        thrust_vec = Vec2d(0, 1) * self.body.angle
        if self.jet_propel(thrust_vec):
            self.voltage = self.action_potential_baseline
        elif not self.jet_propel(thrust_vec):
            self.voltage += self.threshold_update()