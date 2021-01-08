import os, sys, pygame


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
right_st = load_image("cheese_stand11.png")
right_go1 = load_image("cheese_go11.png")
right_go2 = load_image("cheese_go12.png")
left_st = load_image("cheese_stand21.png")
left_go1 =  load_image("cheese_go21.png")
left_go2 =  load_image("cheese_go22.png")


class Cheese_Go(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = left_st
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 200
        self.cur_frame = 0
        self.cheese_list = [right_st, right_go1, right_go2,
                            left_st, left_go1, left_go2]

    def update(self, *args):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            if self.cur_frame >= 3:
                self.cur_frame = 0
            self.image = self.cheese_list[self.cur_frame]
            self.cur_frame += 1
            self.rect.x += 8
        elif not(keys[pygame.K_RIGHT]):
            if keys[pygame.K_LEFT]:
                if self.cur_frame < 3 or self.cur_frame == 6:
                    self.cur_frame = 3
                self.image = self.cheese_list[self.cur_frame]
                self.cur_frame += 1
                self.rect.x -= 8
            else:
                if self.image == self.cheese_list[1]\
                    or self.image == self.cheese_list[2]:
                    self.image = self.cheese_list[0]
                elif self.image == self.cheese_list[4]\
                    or self.image == self.cheese_list[5]:
                    self.image = self.cheese_list[3]


all_sprites = pygame.sprite.Group()
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
    clock.tick(15)

pygame.quit()