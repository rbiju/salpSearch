import pymunk
import pymunk.pygame_util
import pygame

space = pymunk.Space()
space.gravity = 0, -900


def info(body):
    print(f'm={body.mass:.0f} moment={body.moment:.0f}')
    cg = body.center_of_gravity
    print(cg.x, cg.y)


class Box:
    def __init__(self, p0=(10, 10), p1=(690, 230), d=2):
        x0, y0 = p0
        x1, y1 = p1
        pts = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
        for i in range(4):
            segment = pymunk.Segment(space.static_body, pts[i], pts[(i + 1) % 4], d)
            segment.elasticity = 1
            segment.friction = 1
            space.add(segment)


class Polygon:
    def __init__(self, pos, vertices, density=0.1):
        self.body = pymunk.Body(1, 100)
        self.body.position = pos

        shape = pymunk.Poly(self.body, vertices)
        shape.density = 0.1
        shape.elasticity = 1
        space.add(self.body, shape)


class Rectangle:
    def __init__(self, pos, size=(80, 50)):
        self.body = pymunk.Body()
        self.body.position = pos

        shape = pymunk.Poly.create_box(self.body, size)
        shape.density = 0.1
        shape.elasticity = 1
        shape.friction = 1
        space.add(self.body, shape)


class App:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((700, 240))
        self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)
        self.running = True

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill((220, 220, 220))
            space.debug_draw(self.draw_options)
            pygame.display.update()
            space.step(0.01)

        pygame.quit()


if __name__ == '__main__':
    Box()

    body = pymunk.Body(mass=1, moment=10)
    body.position = (100, 200)
    body.apply_impulse_at_local_point((200, 0))

    circle = pymunk.Circle(body, radius=20)
    circle.elasticity = 0.95
    circle.friction = 1
    space.add(body, circle)

    info(body)
    App().run()
