from abc import ABC, abstractmethod

from math import radians

import pygame
import pymunk
from pymunk.constraints import DampedSpring, RotaryLimitJoint, PinJoint
from helpers import FastFunctions, convert_coordinates


# Render Handlers
class RenderHandler(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get_game_position(self, physics_position):
        raise NotImplementedError

    @abstractmethod
    def draw_salp(self, salp):
        raise NotImplementedError

    @abstractmethod
    def draw_connection(self, salp1, salp2):
        raise NotImplementedError


class PygameHandler(RenderHandler):
    def __init__(self):
        super().__init__()
        self.disp = 800
        self.screen = pygame.display.set_mode((self.disp, self.disp))

    def get_game_position(self, physics_position):
        x, y = convert_coordinates(physics_position, self.disp)
        return x, y

    def draw_salp(self, salp):
        x, y = convert_coordinates(salp.body.position, self.disp)
        pygame.draw.circle(self.screen, (153, 255, 204), (x, y), salp.radius)

    def draw_connection(self, salp1, salp2):
        pygame.draw.aaline(self.screen, (0, 0, 0), self.get_game_position(salp1), self.get_game_position(salp2))


# Physics Handlers
class CreaturePhysicsHandler(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def create_body(self, radius, pos):
        raise NotImplementedError

    @abstractmethod
    def add_body(self, body, shape):
        raise NotImplementedError


class LinkHandler(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def add_link(self, body1, body2):
        raise NotImplementedError


class SalpPhysicsHandler(CreaturePhysicsHandler):
    def __init__(self, space: pymunk.Space):
        super().__init__()
        self.space = space

    def create_body(self, radius, pos):
        body = pymunk.Body(mass=1, moment=10)
        body.position = pos
        shape = pymunk.Circle(body, radius)
        shape.density = 1
        self.add_body(body, shape)

        return body

    def add_body(self, body, shape):
        self.space.add(body, shape)


class PinHandler(LinkHandler):
    def __init__(self, space: pymunk.Space):
        super().__init__()
        self.space = space

    def add_link(self, body1, body2):
        link = PinJoint(body1, body2, (0, 0), (0, 0))
        self.space.add(link)


class RotaryLimitHandler(LinkHandler):
    def __init__(self, space: pymunk.Space):
        super().__init__()
        self.space = space
        self._max = radians(-20)
        self._min = radians(20)

    @property
    def _min(self):
        return self._min

    @_min.setter
    def _min(self, _min):
        self._min = _min

    @property
    def _max(self):
        return self._max

    @_max.setter
    def _max(self, _max):
        self._max = _max

    def add_link(self, body1, body2):
        link = RotaryLimitJoint(body1, body2, min=self._min, max=self._max)
        self.space.add(link)


class DampedSpringHandler(LinkHandler):
    def __init__(self, space: pymunk.Space):
        super().__init__()
        self.space = space
        self.stiffness = 200
        self.damping = 20

    @property
    def stiffness(self):
        return self.stiffness

    @stiffness.setter
    def stiffness(self, stiffness):
        self.stiffness = stiffness

    @property
    def damping(self):
        return self.damping

    @damping.setter
    def damping(self, damping):
        self.damping = damping

    def add_link(self, body1, body2):
        rest_length = (body1.pos - body2.pos).length
        link = DampedSpring(body1, body2, (0, 0), (0, 0), rest_length=rest_length,
                            stiffness=self.stiffness, damping=self.damping)
        self.space.add(link)


# Concentration Handlers
class ConcentrationHandler(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get_conc(self, pos):
        raise NotImplementedError


class FicksConcentrationHandler(ConcentrationHandler):
    def __init__(self):
        super().__init__()
        self.ff = FastFunctions()
        self.origin = None
        self.t = None
        self.D = None
        self.scale_factor = 500

    def scale_position(self, pos):
        return pos.x / self.scale_factor, pos.y / self.scale_factor

    def get_conc(self, pos):
        return self.ff.ficks(self.scale_position(pos), self.scale_position(self.origin), self.t, self.D)
