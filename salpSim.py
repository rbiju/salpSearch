import numpy as np
import pygame
import pymunk
import math
from numba import jit
from pymunk.vec2d import Vec2d
from pymunk.constraints import DampedSpring


space = pymunk.Space()
space.damping = 0.8
disp = 800
screen = pygame.display.set_mode((disp, disp))
pygame.display.set_caption('Salp Search Simulation')


def convert_coordinates(point, dispY):
    return int(point[0]), int(dispY - point[1])


@jit(nopython=True)
def get_concentration_at_point(point, origin, t, D):
    l2 = (point[0] - origin[0]) ** 2 + (point[1] - origin[1]) ** 2
    if t == 0:
        return 255
    else:
        return int((60 / (math.sqrt(12.56 * D * t))) * np.exp(-l2 / (4 * D * t)))


@jit(nopython=True)
def get_concentration_array(shape, origin, t, D):
    rows, columns = shape
    alphaArr = np.zeros((rows, columns), dtype=np.int32)
    for i in range(rows):
        for j in range(columns):
            point_conc = 255 - get_concentration_at_point((i / rows, j / columns), origin, t, D)
            if point_conc < 0:
                alphaArr[i, j] = 0
            else:
                alphaArr[i, j] = point_conc
    return alphaArr


@jit(nopython=True)
def gray(im):
    w, h = im.shape
    ret = np.empty((w, h, 3), dtype=np.uint8)
    ret[:, :, 2] = ret[:, :, 1] = ret[:, :, 0] = im
    return ret


class Salp:
    def __init__(self, radius, thrust, pos):
        self.radius = radius
        self.thrust = thrust
        self.body = pymunk.Body(mass=1, moment=10)
        self.body.position = pos
        self.shape = pymunk.Circle(self.body, self.radius)
        self.shape.density = 1
        self.default_threshold = 0.0001
        self.threshold_constant = 0.0003
        self.threshold = self.default_threshold
        space.add(self.body, self.shape)

    def draw(self):
        x, y = convert_coordinates(self.body.position, disp)
        pygame.draw.circle(screen, (153, 255, 204), (x, y), self.radius)

    def get_game_position(self):
        x, y = convert_coordinates(self.body.position, disp)
        return x, y

    def get_normalized_position(self):
        x, y = self.get_game_position()
        return x / disp, y / disp

    def getSalpConc(self, origin, t, D):
        return get_concentration_at_point(self.get_normalized_position(), origin, t, D)

    def jetPropel(self, thrustVec, threshold, seed):
        if seed < threshold:
            self.body.apply_impulse_at_local_point(thrustVec * self.thrust, (0, 0))
            return True
        else:
            return False

    def thresholdUpdate(self, origin, t, D):
        salpConc = self.getSalpConc(origin, t, D) / 255
        thresholdAdd = self.threshold_constant * (1 - self.default_threshold) * (1 - np.tanh(salpConc))
        return thresholdAdd

    def jetDecision(self, origin, t, D, thrustVec):
        seed = np.random.rand()
        if self.jetPropel(thrustVec, self.threshold, seed):
            self.threshold = self.default_threshold
        elif not self.jetPropel(thrustVec, self.threshold, seed):
            self.threshold += self.thresholdUpdate(origin, t, D)


# class for creating salp chain, grown from initial salp
# forms chain of length number * 2 + 1
# noinspection PyArgumentList

class SalpChain:
    def __init__(self, startVec: tuple, number, startPos: tuple, thresholdConst, defaultThresh):
        vecx, vecy = startVec
        self.startVec = Vec2d(vecx, vecy).normalized()
        self.number = number
        posx, posy = startPos
        self.startPos = Vec2d(posx, posy)
        self.distance = 15
        self.thrust = 1500
        self.threshold_const = thresholdConst
        self.default_threshold = defaultThresh
        self.salpList = []
        self.beamList = []
        self.flipDirection = True

    def makeChain(self):
        firstPos = self.startPos - (self.number * self.distance * self.startVec)
        for i in range(0, 2 * self.number + 1):
            salp = Salp(5, self.thrust, firstPos + (i * self.distance * self.startVec))
            salp.threshold_constant = self.threshold_const
            salp.default_threshold = self.default_threshold
            salp.draw()
            self.salpList.append(salp)

    def makeConnections(self):
        for i in range(0, len(self.salpList) - 1):
            salp1 = self.salpList[i]
            salp2 = self.salpList[i + 1]
            spring = DampedSpring(salp1.body, salp2.body, (0, 0), (0, 0), self.distance, 200, 20)
            pygame.draw.aaline(screen, (0, 0, 0), salp1.get_game_position(), salp2.get_game_position())
            space.add(spring)

    def getThrustVec(self):
        chainVec = Vec2d(0, 0)
        salp1 = self.salpList[0]
        salp2 = self.salpList[-1]
        p1x, p1y = salp1.body.position
        p2x, p2y = salp2.body.position
        if self.flipDirection:
            chainVec = Vec2d(p2x, p2y) - Vec2d(p1x, p1y)
        elif not self.flipDirection:
            chainVec = Vec2d(p1x, p1y) - Vec2d(p2x, p2y)
        thrustVec = chainVec.perpendicular_normal()
        return thrustVec

    def drawChain(self):
        for i in range(0, len(self.salpList) - 1):
            salp1 = self.salpList[i]
            salp1.draw()
            salp2 = self.salpList[i + 1]
            salp2.draw()
            pygame.draw.aaline(screen, (0, 0, 0), salp1.get_game_position(), salp2.get_game_position())

    def chainThrust(self, origin, t, D):
        for salp in self.salpList:
            salp.jetDecision(origin, t, D, self.getThrustVec())

    def pushSalp(self, ndx):
        salp = self.salpList[ndx]
        salp.jetPropel(self.getThrustVec(), 0.9, 0.5)

    def getCenterPos(self):
        centerNDx = int(len(self.salpList) / 2)
        return self.salpList[centerNDx].get_game_position()


class App:
    def __init__(self, FPS, salpNum, thresholdConst, defaultThresh, thrust, distance):
        pygame.init()
        self.running = True
        self.fps = FPS
        self.clock = pygame.time.Clock()
        self.clickPos = (0, 0)
        self.unitClickPos = self.clickPos
        self.clickTime = 0
        self.clickFlag = False
        self.diffCoeff = 0.0007
        get_concentration_at_point((1, 1), (20, 20), 1, 0.1)  # dummy calls to compile numba function
        get_concentration_array((10, 10), (5, 5), 2, 0.1)
        self.salpChain = SalpChain((1, 1), salpNum, (400, 400), thresholdConst, defaultThresh)
        self.salpChain.thrust = thrust
        self.salpChain.distance = distance
        self.salpChain.makeChain()
        self.salpChain.makeConnections()
        self.fitness = 0

    def getFitness(self):
        centerPos = self.salpChain.getCenterPos()
        posVec = Vec2d(self.clickPos) - Vec2d(centerPos)
        return posVec.length

    def run(self):
        columns, rows = pygame.display.get_window_size()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if not self.clickFlag:
                        self.clickPos = pygame.mouse.get_pos()
                        self.unitClickPos = (self.clickPos[0] / rows, self.clickPos[1] / columns)
                        self.clickTime = pygame.time.get_ticks()
                        self.clickFlag = not self.clickFlag
                    else:
                        self.clickFlag = not self.clickFlag

            screen.fill((255, 255, 255))
            if self.clickFlag:
                loopTime = pygame.time.get_ticks()
                t = (loopTime - self.clickTime) / 1000
                if t > 10:
                    self.fitness = self.getFitness()
                    break
                arr = get_concentration_array((rows, columns), self.unitClickPos, t, self.diffCoeff)
                grayscaleArr = gray(arr)
                pygame.surfarray.blit_array(screen, grayscaleArr)
                self.salpChain.chainThrust(self.unitClickPos, t, self.diffCoeff)

            self.salpChain.drawChain()
            pygame.display.update()
            self.clock.tick(self.fps)
            space.step(1 / self.fps)

        print(pygame.display.get_window_size())
        pygame.quit()


if __name__ == '__main__':
        App(15, 3, 0.0004, 0.002, 1000, 10).run()
