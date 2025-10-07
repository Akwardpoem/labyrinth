#создай игру "Лабиринт"!
from pygame import *

class GameSprite(sprite.Sprite):
    def __init__(self,player_image,player_x,player_y,player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65,65))
        self.player_speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_w] and self.rect.y > 5:
            self.rect.y -= self.player_speed
        if keys_pressed[K_a] and self.rect.x > 5:
            self.rect.x -= self.player_speed
        if keys_pressed[K_s] and self.rect.y < 425:
            self.rect.y += self.player_speed
        if keys_pressed[K_d] and self.rect.x < 625:
            self.rect.x += self.player_speed

class Enemy(GameSprite):
    def __init__(self,player_image,player_x,player_y,player_speed):
        super().__init__(player_image,player_x,player_y,player_speed)
        self.direction = 'left'
        
    def update(self):
        if self.rect.x < 450:
            self.direction = 'right'
        if self.rect.x > 625:
            self.direction = 'left'
        if self.direction == 'left':
            self.rect.x -= self.player_speed
        else:
            self.rect.x += self.player_speed

class Wall(sprite.Sprite):
    def __init__(self, color_1, color_2, color_3, width, height, x, y):
        super().__init__()
        self.color = (color_1,color_2,color_3)
        self.width = width
        self.height = height
        self.image = Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def place(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

window = display.set_mode((700,500))
display.set_caption('Лабиринт')
clock = time.Clock()
background = transform.scale(image.load("background.jpg"),(700,500))

game = True
FPS = 60
finish = False
font.init()
font = font.Font(None, 70)

mixer.init()
mixer.music.load("jungles.ogg")
money = mixer.Sound("money.ogg")
kick = mixer.Sound("kick.ogg")
#mixer.music.play()

player = Player("hero.png",60,370,5)
enemy = Enemy('cyborg.png', 600, 300, 2)
treasure = GameSprite('treasure.png', 550, 400, 0)

wall1 = Wall(32, 192, 124, 15, 500, 15, 15)
wall2 = Wall(32, 192, 124, 400, 15, 15, 15)
wall3 = Wall(32, 192, 124, 15, 300, 180, 200)
wall4 = Wall(32, 192, 124, 15, 350, 280, 15)
wall5 = Wall(32, 192, 124, 15, 350, 420, 150)
wall6 = Wall(32, 192, 124, 420, 15, 15, 490)

while game:
    collide_wall = sprite.collide_rect(player, wall1) or sprite.collide_rect(player, wall2) or sprite.collide_rect(player, wall3) or sprite.collide_rect(player, wall4) or sprite.collide_rect(player, wall5) or sprite.collide_rect(player, wall6)
    for e in event.get():
        if e.type == QUIT:
            game = False

    if finish != True:
        
        window.blit(background,(0,0))
        
        enemy.update()
        player.update()

        wall1.place()
        wall2.place()
        wall3.place()
        wall4.place()
        wall5.place()
        wall6.place()

        player.reset()
        enemy.reset()
        treasure.reset()

        if sprite.collide_rect(player, enemy) or collide_wall:
            finish = True
            window.blit(font.render('YOU LOSE!', True, (255, 0, 0)), (200,215))
            kick.play()
        
        if sprite.collide_rect(player, treasure):
            finish = True
            window.blit(font.render('YOU WIN!', True, (236, 233, 36)), (200,215))
            money.play()
        
    clock.tick(FPS)
    display.update()