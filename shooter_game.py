from pygame import *
from random import *
from time import time as tm 

#создай окно игры
window = display.set_mode((700, 500))
display.set_caption('Шутер')

#задай фон сцены
background = transform.scale(image.load('galaxy.jpg'),(700, 500))

#создай 2 спрайта и размести их на сцене
#sprite1 = transform.scale(image.load('sprite1.png'), (100, 100))

#МУзыка
mixer.init()
mixer.music.load('space.ogg')
fire_m = mixer.Sound('fire.ogg')

lost = 0
score = 0
font.init()
font1 = font.SysFont('Arial', 70)
font2 = font.SysFont('Arial', 30)

win = font1.render('YOU WIN!', True, (155, 215, 0))
loss = font1.render('YOU LOSS', True, (255, 50, 0))

#mixer.music.play()


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, w, h, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), ( w , h ))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        key_pressed = key.get_pressed()
        if key_pressed[K_a] and self.rect.x > 5:
            self.rect.x -= 10
        if key_pressed[K_d] and self.rect.x < 635:
            self.rect.x += 10
    def fire(self):
        bullet = Bullet('bullet.png' , self.rect.centerx, self.rect.top, 15 , 20, -15)
        bullets.add(bullet)

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y <= 0:
            self.kill()

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y >= 500:
            self.rect.y = 0 
            lost += 1
            self.rect.x = randint(0, 635)


class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= 500:
            self.rect.y = 0 
      
            self.rect.x = randint(0, 635)

asteroids = sprite.Group()
bullets = sprite.Group()          
monsters = sprite.Group()
player = Player("rocket.png", 5, 435, 40, 60 ,  4)

for i in range(5):
    enemy = Enemy("ufo.png", randint(0, 635) , 0 , 50 , 40 ,  randint(1, 2))   
    monsters.add(enemy)


for i in range(3):
    asteroid = Asteroid("asteroid.png ", randint(0, 635) , 0 , 50 , 40 ,  randint(1, 3))   
    asteroids.add(asteroid)

#обработай событие «клик по кнопке "Закрыть окно"»
num_fire = 0
rel_time = False
clock = time.Clock()
FPS = 60
game = True
finish = False

while game:
    for i in event.get():
        if i.type  == QUIT:
            game = False
        elif i.type == KEYDOWN:
            if i.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    
                    player.fire()
                    num_fire += 1
                    #fire_m.play()
                if num_fire >= 5 and rel_time == False:
                    rel_time = True
                    old_time = tm()
                    
        
    if finish != True:
        window.blit(background, (0, 0))
        player.update()
        player.reset()

        monsters.update()
        monsters.draw(window)
        bullets.update()
        bullets.draw(window)
        asteroids.update()
        asteroids.draw(window)

        if rel_time == True:
            new_time = tm()
            if new_time - old_time < 2:
                rel = font1.render('wait reload...'+str(int(new_time - old_time)), True, (255, 50, 0))
                window.blit(rel, (200, 450))
            else:
                num_fire = 0
                rel_time = False

        sprites_list = sprite.groupcollide(
            monsters, bullets, True, True
        )
        
        for i in sprites_list:
            score += 1
            enemy = Enemy("ufo.png", randint(0, 635) , 0 , 50 , 40 ,  randint(1, 4))   
            monsters.add(enemy)

        if score >= 10:
            finish = True
            window.blit(win, (200, 200) )
        if lost >= 3 or  sprite.spritecollide(player, monsters, False) or sprite.spritecollide(player, asteroids, False):
            finish = True
            window.blit(loss, (200, 200) )
        lostt = font2.render('Пропущенно: '+str(lost), True, (155, 215, 0))
        scorr = font2.render('Счёт: '+str(score), True, (155, 215, 0))
        window.blit(lostt, (0, 0))
        window.blit(scorr, (0, 30))
    clock.tick(FPS)
    display.update()
