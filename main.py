import os, sys, pygame, time


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
latest_move = 'left'
right_st = load_image("cheese_stand11.png")
right_go1 = load_image("cheese_go11.png")
right_go2 = load_image("cheese_go12.png")
left_st = load_image("cheese_stand21.png")
left_go1 =  load_image("cheese_go21.png")
left_go2 =  load_image("cheese_go22.png")
gun_left = load_image("gun1.png")
gun_right = load_image("gun2.png")
bull = load_image("bullet.png")


all_sprites = pygame.sprite.Group()


class Cheese_Go(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = left_st
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 200
        self.cur_frame = 3
        self.cheese_list = [right_st, right_go1, right_go2,
                            left_st, left_go1, left_go2]

    def update(self, *args):
        global latest_move
        global my_bull
        keys = pygame.key.get_pressed()

        if my_bull.rect.x < 0 or my_bull.rect.x > width:
            if 0 <= self.cur_frame <= 2:
                latest_move = 'right'
            elif 3 <= self.cur_frame <= 5:
                latest_move = 'left'

        if keys[pygame.K_RIGHT]:
            self.image = self.cheese_list[self.cur_frame]
            self.cur_frame += 1
            self.rect.x += 8
            if self.cur_frame >= 3:
                self.cur_frame = 0
        elif not(keys[pygame.K_RIGHT]):
            if keys[pygame.K_LEFT]:
                self.image = self.cheese_list[self.cur_frame]
                self.cur_frame += 1
                self.rect.x -= 8
                if self.cur_frame < 3 or self.cur_frame == 6:
                    self.cur_frame = 3
            else:
                if self.image == self.cheese_list[1]\
                    or self.image == self.cheese_list[2]:
                    self.image = self.cheese_list[0]
                elif self.image == self.cheese_list[4]\
                    or self.image == self.cheese_list[5]:
                    self.image = self.cheese_list[3]


my_cheese = Cheese_Go(all_sprites)


class Gun(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = gun_left
        self.rect = self.image.get_rect()
        self.rect.x = 300
        self.rect.y = 300

    def update(self, *args):
        global my_cheese
        if 3 <= my_cheese.cur_frame <= 5:
            self.image = gun_left
            self.rect.x = my_cheese.rect.x + 99
            self.rect.y = my_cheese.rect.y + 90
        elif 0 <= my_cheese.cur_frame <= 2:
            self.image = gun_right
            self.rect.x = my_cheese.rect.x + 39
            self.rect.y = my_cheese.rect.y + 90

my_gun = Gun(all_sprites)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = bull
        self.rect = self.image.get_rect()
        self.rect.x = -1
        self.rect.y = my_gun.rect.y + 2

    def update(self, *args):
        if my_bull.rect.x < 0 or my_bull.rect.x > width:
            my_bull.rect.x = -50

        v = 8.5
        keys = pygame.key.get_pressed()

        if keys[pygame.K_f]:
            if my_bull.rect.x < 0 or my_bull.rect.x > width:
                if latest_move == 'left':
                    my_bull.rect.x = my_gun.rect.x
                elif latest_move == 'right':
                    my_bull.rect.x = my_gun.rect.x + 45

        if latest_move == 'left':
            my_bull.rect.x -= v
        elif latest_move == 'right':
            my_bull.rect.x += v


my_bull = Bullet(all_sprites)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running  = False

    screen.fill('white')
    all_sprites.draw(screen)
    all_sprites.update(event)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()