import random
import pygame as pg
from os import path

img_dir = path.join(path.dirname(__file__), 'img')

WIDTH = 400
HEIGHT = 700
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Flappy Bird!")
clock = pg.time.Clock()


class Bird(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)

        self.image = pg.image.load(path.join(img_dir, "Bird1.png")).convert()
        self.image.set_colorkey(PURPLE)
        self.image = pg.transform.scale(self.image, (50, 40))

        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = 40

        self.birdY = 350
        self.jump = 0
        self.jumpSpeed = 15
        self.gravity = 5
        self.gravity_k = 0.2

    def jump_set(self):
        self.jump = 30
        self.gravity = 5
        self.jumpSpeed = 15

    def update(self):
        if self.jump:
            self.jumpSpeed -= 1
            self.birdY -= self.jumpSpeed
            self.jump -= 1
        else:
            self.birdY += self.gravity
            self.gravity += self.gravity_k
        self.rect.y = self.birdY

        if self.rect.y > 700 or self.rect.y < 0:
            self.kill()


class Column(pg.sprite.Sprite):
    def __init__(self, side):
        pg.sprite.Sprite.__init__(self)

        self.score = 0

        self.side = side
        self.gap = 140
        self.offset = random.randint(50, 130)
        self.wallx_start = 400
        self.speed = 2

        self.image = pg.image.load(path.join(img_dir, "Column1.png")).convert()
        self.image.set_colorkey(WHITE)
        self.image = pg.transform.scale(self.image, (80, 420))

        self.rect = self.image.get_rect()

        self.start()

    def update(self):
        self.rect.x -= self.speed
        if self.rect.x < -80:
            self.score += 1
            self.start()

    def start(self):
        self.speed = 2
        self.offset = random.randint(50, 130)
        if self.side == "top":
            self.rect.y = 360 + self.gap - self.offset + 10
        elif self.side == "bot":
            self.rect.y = 0 - self.gap - self.offset - 1

        self.rect.x = self.wallx_start


all_sprites = pg.sprite.Group()
columns = pg.sprite.Group()

for i in ["top", "bot"]:
    column = Column(i)
    all_sprites.add(column)
    columns.add(column)

bird = Bird()
all_sprites.add(bird)

running = True
while running:
    clock.tick(FPS)
    for event in pg.event.get():

        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN or event.type == pg.MOUSEBUTTONUP:
            bird.jump_set()

    all_sprites.update()

    screen.fill(BLACK)
    all_sprites.draw(screen)
    pg.display.flip()

pg.quit()
