import os, sys, pygame, time
from random import randint


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
size = width, height = 700, 500
screen = pygame.display.set_mode(size)
screen.fill('white')
pygame.display.set_caption('Сыр')
clock = pygame.time.Clock()
latest_move = 'left'
health = 300
score = 0
v = 10
now_go = 0
back = load_image("back.png")
right_st = load_image("cheese_stand11.png")
right_go1 = load_image("cheese_go11.png")
right_go2 = load_image("cheese_go12.png")
left_st = load_image("cheese_stand21.png")
left_go1 =  load_image("cheese_go21.png")
left_go2 =  load_image("cheese_go22.png")
gun_left = load_image("gun1.png")
gun_right = load_image("gun2.png")
bull = load_image("bullet.png")
rat_right = load_image("rat1.png")
rat_left = load_image("rat2.png")
rat_right2 = load_image("rat12.png")
rat_left2 = load_image("rat22.png")
rats_list = [rat_right, rat_left, rat_right2, rat_left2]

for_play = pygame.font.SysFont('freesansbold.ttf', 40)
for_play = for_play.render('PLAY', True, (0, 0, 0))
for_loss = pygame.font.SysFont('freesansbold.ttf', 40)
for_loss = for_loss.render('GAME OVER', True, (0, 0, 0))

all_sprites = pygame.sprite.Group()

class Cheese_Go(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = left_st
        self.rect = self.image.get_rect()
        self.rect.x = width / 2 - 100
        self.rect.y = 200
        self.cur_frame = 3
        self.cheese_list = [right_st, right_go1, right_go2,
                            left_st, left_go1, left_go2]
        self.mask = pygame.mask.from_surface(self.image)


    def update(self, *args):
        global health
        if pygame.sprite.collide_mask(self, rat):
            health -= 5
        global latest_move
        global my_bull
        keys = pygame.key.get_pressed()

        if my_bull.rect.x < 0 or my_bull.rect.x > width or v == 0:
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
        clock.tick(90)


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
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = 1000
        self.rect.y = my_gun.rect.y + 2

    def update(self, *args):
        global v
        if my_bull.rect.x < 0 or my_bull.rect.x > width or v == 0:
            my_bull.rect.x = 10000

        keys = pygame.key.get_pressed()

        if keys[pygame.K_f]:
            if my_bull.rect.x < 0 or my_bull.rect.x > width or v == 0:
                if latest_move == 'left':
                    my_bull.rect.x = my_gun.rect.x
                elif latest_move == 'right':
                    my_bull.rect.x = my_gun.rect.x + 45
                v = 10


        if latest_move == 'left':
            my_bull.rect.x -= v
        elif latest_move == 'right':
            my_bull.rect.x += v


class Rats(pygame.sprite.Sprite):
    global rats_list

    def more_inits(self):
        self.dir = randint(0, 1)
        self.image = rats_list[self.dir]
        self.where = 2 if self.dir == 0 else -2
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = -120 if self.dir == 0 else width - 10
        self.rect.y = 230

    def __init__(self, group):
        super().__init__(group)
        self.more_inits()
        self.a = 0

    def update(self, *args):
        global score, v, latest_move
        if pygame.sprite.collide_mask(self, my_bull):
            self.more_inits()
            score += 1
            my_bull.rect.x = 100
            v = 0

        if self.a % 6 == 0:
            self.image = rats_list[self.dir + 2]
        else:
            self.image = rats_list[self.dir]
        self.rect.x += self.where
        self.a += 1


rat = Rats(all_sprites)

my_bull = Bullet(all_sprites)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running  = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pos() >= (width / 2 - 100, height / 2 - 50):
                if pygame.mouse.get_pos() <= (width / 2 + 100, height / 2 + 50):
                    now_go = 1
    screen.blit(back, (0, 0))
    if now_go == 1:
        pygame.draw.rect(screen, (255, 0, 0), (20, 450, 300, 30), border_radius=5)
        pygame.draw.rect(screen, (0, 255, 0), (20, 450, health, 30), border_radius=5)
        all_sprites.draw(screen)
        my_cheese.mask = pygame.mask.from_surface(my_cheese.image)
        font_score = pygame.font.SysFont('freesansbold.ttf', 40)
        txt_score = font_score.render('Score:   ' + str(score), True, (0, 0, 0))
        screen.blit(txt_score, (500, 450))
        if health == 0:
            now_go = 2
        all_sprites.update(event)
    elif now_go == 0:
        pygame.draw.rect(screen, (0, 100, 200), (width / 2 - 100, height / 2 - 50, 200, 100),
                         border_radius=20)
        screen.blit(for_play, (width / 2 - 35, height / 2 - 15))
    else:
        pygame.draw.rect(screen, (0, 100, 200), (width / 2 - 140, height / 2 - 100, 300, 200),
                         border_radius=20)
        screen.blit(for_loss, (width / 2 - 70, height / 2 - 60))
        screen.blit(txt_score, (width / 2 - 52, height / 2 + 20))
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
