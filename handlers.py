from abc import ABC, abstractmethod

import pygame
import pymunk
from helpers import FastFunctions, convert_coordinates


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


class PhysicsHandler(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def create_body(self, radius, pos):
        raise NotImplementedError

    @abstractmethod
    def add_body(self, body, shape):
        raise NotImplementedError


class SalpPhysicsHandler(PhysicsHandler):
    def __init__(self):
        super().__init__()
        self.space = pymunk.Space()

    def create_body(self, radius, pos):
        body = pymunk.Body(mass=1, moment=10)
        body.position = pos
        shape = pymunk.Circle(body, radius)
        shape.density = 1
        self.add_body(body, shape)

        return body

    def add_body(self, body, shape):
        self.space.add(body, shape)


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
