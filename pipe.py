import pygame as pg
import os
import random


PIPE_IMG = pg.transform.scale2x(pg.image.load(os.path.join("IMG", "pipe.png")))

#Pipe - klasa opisująca mechanikę przeszkód
class Pipe:
    gap = 180
    vel = 5

    def __init__(self, x):
        self.x = x
        self.height = 0

        self.top = 0
        self.bottom = 0
        self.pipe_top = pg.transform.flip(PIPE_IMG, False, True)
        self.pipe_bottom = PIPE_IMG

        self.passed = False
        self.set_height()

# set_height - metoda do określenia losowego wyświetlania
# przeszkód
    def set_height(self):
        self.height = random.randrange(100, 360)
        self.top = self.height - self.pipe_top.get_height()
        self.bottom = self.height + self.gap

# move - metoda określająca mechanikę poruszania się przeszkód
    def move(self):
        self.x -= self.vel

# draw - metoda odpowiadająca za wyświetlanie grafiki przeszkody
    def draw(self, window):
        window.blit(self.pipe_top, (self.x, self.top))
        window.blit(self.pipe_bottom, (self.x, self.bottom))

# collide - metoda służąca do wykrywania kolizji, wykorzystywana jest
#metoda get_mask klasy Bird aby uzyskać największą precyzje
#zderzenia
    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pg.mask.from_surface(self.pipe_top)
        bottom_mask = pg.mask.from_surface(self.pipe_bottom)

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)

        if t_point or b_point:
            return True

        return False