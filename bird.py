import pygame as pg
import os
import net

BIRD_IMGS = [pg.transform.scale2x(pg.image.load(os.path.join("IMG", "bird1.png"))),
             pg.transform.scale2x(pg.image.load(os.path.join("IMG", "bird2.png"))),
             pg.transform.scale2x(pg.image.load(os.path.join("IMG", "bird3.png")))]

#Bird - klasa opisująca mechanikę obiektu, którym sterujemy
class Bird:
    IMGS = BIRD_IMGS
    max_rotation = 25
    rot_vel = 20
    animation_time = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]
        self.tick_count = 0
        self.net = net.Net()
        self.score = 0
        self.is_alive = True

    def revive(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]
        self.tick_count = 0
        self.score = 0
        self.is_alive = True

#jump - metoda odpowiadająca za mechanikę skoku w
# momencie impulsu sterującego

    def jump(self):
        self.vel = -13
        self.tick_count = 0
        self.height = self.y

#move - metoda określająca zmianę położenia w okresie
# jednej klatki
    def move(self):
        self.tick_count += 1
        d = self.vel * self.tick_count + 2 * self.tick_count ** 2

        if d >= 11:
            d = (d / abs(d)) * 11

        if d < 0:
            d -= 5

        self.y = self.y + d

        if d < 0 or self.y < self.height + 50:
            if self.tilt < self.max_rotation:
                self.tilt = self.max_rotation
        else:
            if self.tilt > -60:
                self.tilt -= self.rot_vel

#draw - metoda, dzięki której jest wyświetlana
# animacja lotu oraz opadania w przypadku braku reakcji na impuls skoku
    def draw(self, window):
        self.img_count += 1

        if self.img_count <= self.animation_time:
            self.img = self.IMGS[0]
        elif self.img_count <= self.animation_time * 2:
            self.img = self.IMGS[1]
        elif self.img_count <= self.animation_time * 3:
            self.img = self.IMGS[2]
        elif self.img_count <= self.animation_time * 4:
            self.img = self.IMGS[1]
        elif self.img_count == self.animation_time * 4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        if self.tilt <= -60:
            self.img = self.IMGS[1]
            self.img_count = self.animation_time * 2

        blitRotateCenter(window, self.img, (self.x, self.y), self.tilt)

#get_mask - metoda zwraca maskę obiektu,
# pozwala na uzyskanie zaawansowanej techniki kolizji
    def get_mask(self):
        return pg.mask.from_surface(self.img)


def blitRotateCenter(surf, image, topleft, angle):
    rotated_image = pg.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft=topleft).center)
    surf.blit(rotated_image, new_rect.topleft)