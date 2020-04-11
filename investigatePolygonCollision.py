import pygame
from pygame.math import Vector2
import math

width = 1150
height = 800

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (210, 210, 210)
RED = (255, 0, 0)
GREEN = (20, 255, 140)
BLUE = (0, 0, 255)
GOLD = (255, 215, 0)
SILVER = (192, 192, 192)

drag = 0.999  # Between 0 and 1
elasticity = 0.75  # Between 0 and 1
gravity = (math.pi, 0.000)

pygame.init()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()


# Define game object class
class Circle:
    def __init__(self, coordinates, velocity, angle, radius, objectColor):
        self.x = coordinates[0]
        self.y = coordinates[1]
        self.velocity = velocity
        self.angle = angle
        self.radius = radius
        self.objectColor = objectColor
        self.initSurface = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
        self.rectangle = self.initSurface.get_rect(center=Vector2(self.x, self.y))
        self.surface = self.initSurface
        self.mask = None
        self.draw()

    def draw(self):
        pygame.draw.circle(self.initSurface, self.objectColor, [self.radius, self.radius], self.radius)
        self.mask = pygame.mask.from_surface(self.initSurface)

    def move(self):
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        self.velocity = Vector2(self.velocity) * drag
        self.rectangle.center = Vector2(self.x, self.y)

    def rotate(self, angle):
        self.angle += angle
        self.velocity.rotate_ip(-angle)
        surface = pygame.transform.rotate(self.initSurface, self.angle)
        self.rectangle = surface.get_rect(center=self.rectangle.center)
        self.mask = pygame.mask.from_surface(surface)
        self.surface = surface

    def bounce(self):
        # Right boundary
        if self.x > width - self.radius:
            self.x = 2 * (width - self.radius) - self.x
            self.angle = - self.angle
            self.velocity = Vector2(self.velocity) * elasticity

        # Left boundary
        elif self.x < self.radius:
            self.x = 2 * self.radius - self.x
            self.angle = - self.angle
            self.velocity = Vector2(self.velocity) * elasticity

        # Top boundary
        if self.y > height - self.radius:
            self.y = 2 * (height - self.radius) - self.y
            self.angle = math.pi - self.angle
            self.velocity = Vector2(self.velocity) * elasticity

        # Bottom boundary
        elif self.y < self.radius:
            self.y = 2 * self.radius - self.y
            self.angle = math.pi - self.angle
            self.velocity = Vector2(self.velocity) * elasticity


class Polygon:
    def __init__(self, coordinates, velocity, angle, pointList, objectColor):
        self.x = coordinates[0]
        self.y = coordinates[1]
        self.velocity = velocity
        self.angle = angle
        self.pointList = pointList
        self.objectColor = objectColor
        self.initSurface = pygame.Surface((max(self.pointList, key=lambda item: item[0])[0],
                                       max(self.pointList, key=lambda item: item[1])[1]), pygame.SRCALPHA)
        self.rectangle = self.initSurface.get_rect(center=Vector2(self.x, self.y))
        self.surface = self.initSurface
        self.mask = None
        self.draw()

    def draw(self):
        pygame.draw.polygon(self.initSurface, self.objectColor, self.pointList)
        self.mask = pygame.mask.from_surface(self.initSurface)

    def move(self):
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        self.rectangle.center = Vector2(self.x, self.y)

    def rotate(self, angle):
        self.angle += angle
        self.velocity.rotate_ip(-angle)
        surface = pygame.transform.rotate(self.initSurface, self.angle)
        self.rectangle = surface.get_rect(center=self.rectangle.center)
        # We need a new mask after the rotation.
        self.mask = pygame.mask.from_surface(surface)
        self.surface = surface


# Colliding game object particles
def collide(p1, p2):
    offset = p1.rectangle[0] - p2.rectangle[0], p1.rectangle[1] - p2.rectangle[1]
    overlap = myBall.mask.overlap(p1.mask, offset)
    if overlap:
        p2.velocity = Vector2(p1.velocity) * 1.4


# Images
BG_IMG = pygame.Surface((1150, 800))
BG_IMG.fill((30, 120, 30))

# Init Ball and car (input)
myBall = Circle(Vector2(575, 400), Vector2(0, 0), 0, 60, GOLD)
myInput = Polygon(Vector2(470, 370), Vector2(3, 0), 0, [(0, 0), (50, 10), (50, 20), (0, 30)], GOLD)

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        myInput.rotate(5)
    elif keys[pygame.K_RIGHT]:
        myInput.rotate(-5)

    # Move the car
    myInput.move()

    # Move the ball
    myBall.velocity *= .99  # Friction
    myBall.move()
    myBall.bounce()

    # Car collision.
    collide(myInput, myBall)

    # Drawing
    screen.blit(BG_IMG, (0, 0))
    screen.blit(myBall.surface, myBall.rectangle)
    screen.blit(myInput.surface, myInput.rectangle)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
