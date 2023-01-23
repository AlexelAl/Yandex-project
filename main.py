import random
import pygame as pg
from os import path

img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')

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
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Flappy Bird!")
clock = pg.time.Clock()

font_name = pg.font.match_font('arial')


def draw_text(surf, text, size, x, y, color):
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def show_go_screen():
    screen.blit(background, background_rect)
    draw_text(screen, "Flappy Bird!", 64, WIDTH / 2, HEIGHT / 4, BLUE)
    draw_text(screen, "Tap to jump", 44,
              WIDTH / 2, HEIGHT / 2.5, BLUE)
    draw_text(screen, "Press a key to begin", 18, WIDTH / 2, HEIGHT * 3 / 4, BLUE)
    pg.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            if event.type == pg.KEYUP or event.type == pg.MOUSEBUTTONUP:
                waiting = False


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

        self.dead = False
        self.snd_indx = False

    def jump_set(self):
        self.jump = 30
        self.gravity = 5
        self.jumpSpeed = 15

    def update(self):
        if self.jump and not self.dead:
            self.jumpSpeed -= 1
            self.birdY -= self.jumpSpeed
            self.jump -= 1
        else:
            self.birdY += self.gravity
            self.gravity += self.gravity_k
        self.rect.y = self.birdY

        if self.rect.y > 700 or self.rect.y < 0:
            self.kill()

    def die(self):
        self.dead = True
        self.snd_indx = False


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


background = pg.image.load(path.join(img_dir, "Background.png")).convert()
background = pg.transform.scale(background, (400, 700))
background_rect = background.get_rect()

all_sprites = pg.sprite.Group()
columns = pg.sprite.Group()

for i in ["top", "bot"]:
    column = Column(i)
    all_sprites.add(column)
    columns.add(column)

bird = Bird()
all_sprites.add(bird)

hit_snd = pg.mixer.Sound(path.join(snd_dir, 'hit.mp3'))
point_snd = pg.mixer.Sound(path.join(snd_dir, 'point.mp3'))
wing_snd = pg.mixer.Sound(path.join(snd_dir, 'wing.mp3'))
die_snd = pg.mixer.Sound(path.join(snd_dir, 'die.mp3'))

pg.mixer.music.load(path.join(snd_dir, 'music.ogg'))
pg.mixer.music.set_volume(0.4)
pg.mixer.music.play(loops=-1)


game_over = True
running = True
while running:
    if game_over:
        show_go_screen()
        game_over = False
        all_sprites = pg.sprite.Group()
        columns = pg.sprite.Group()

        for i in ["top", "bot"]:
            column = Column(i)
            all_sprites.add(column)
            columns.add(column)

        bird = Bird()
        all_sprites.add(bird)

    clock.tick(FPS)
    for event in pg.event.get():

        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN or event.type == pg.MOUSEBUTTONUP:
            bird.jump_set()
            wing_snd.play()

    all_sprites.update()

    hits = pg.sprite.spritecollide(bird, columns, False)
    if hits:
        bird.dead = True
        for i in columns:
            i.speed = 0.2
        if not bird.snd_indx:
            hit_snd.play()
            bird.snd_indx = True

    if not bird.alive():
        game_over = True
        die_snd.play()

    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(column.score), 45, WIDTH / 2, 10, RED)
    pg.display.flip()

pg.quit()
