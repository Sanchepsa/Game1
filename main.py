import os
import sys

import pygame, time


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


pygame.init()
size = width, height = 500, 500
screen = pygame.display.set_mode(size)
screen.fill('white')
pygame.display.set_caption('Сыр')
clock = pygame.time.Clock()
image1 = load_image("cheese_stand11.png")
image2 = load_image("cheese_go11.png")
image3 = load_image("cheese_go12.png")


class Cheese_Go(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = image1
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 200
        self.cur_frame = 0
        self.cheese_list = [image1, image2, image3]

    def update(self, *args):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.cur_frame = (self.cur_frame + 1) % len(self.cheese_list)
            self.image = self.cheese_list[self.cur_frame]
            self.rect.x += 8
        elif not(keys[pygame.K_RIGHT]):
            self.image = self.cheese_list[0]
        # keys = pygame.key.get_pressed()
        #
        # if keys[pygame.K_LEFT]:
        #     self.image = image2
        #     self.image = image3


all_sprites = pygame.sprite.Group()
# cheese = pygame.sprite.Sprite()
# cheese.image = load_image("cheese_stand11.png")
# cheese.rect = cheese.image.get_rect()
# all_sprites.add(cheese)
# cheese.rect.x = 300
# cheese.rect.y = 300

Cheese_Go(all_sprites)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running  = False

    screen.fill('white')
    all_sprites.draw(screen)
    all_sprites.update(event)

    pygame.display.flip()
    clock.tick(10)

pygame.quit()
