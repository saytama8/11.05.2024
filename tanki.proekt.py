
from pdb import Restart
import pygame
from pygame import *
import sys
import random


mixer.init()
mixer.music.load('5.mp3')
mixer.music.play()

pygame.init()



SCREEN_WIDTH = 900
SCREEN_HEIGHT = 700
FPS = 100
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
background_image = pygame.image.load("22.png")
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

#  фото танка
tank_image = pygame.image.load("31.png")

#  фото ворожих танків
enemy_tank_image = pygame.image.load("88.png")

#  зображення снаряду
bullet_image = pygame.image.load("77.png")


# постріл
shoot_sound = pygame.mixer.Sound("80.mp3") 
killed_tanks = 0

class Tank(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(tank_image, (50, 50)) 
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += 5
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= 5
        if keys[pygame.K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += 5

class EnemyTank(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(enemy_tank_image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(0, SCREEN_HEIGHT - self.rect.height)
        self.speed = random.randint(1, 3)
        self.direction = random.choice(["left", "right", "up", "down"])

    def update(self):
        if self.direction == "left":
            self.rect.x -= self.speed
            if self.rect.x < 0:
                self.direction = "right"
        elif self.direction == "right":
            self.rect.x += self.speed
            if self.rect.x > SCREEN_WIDTH - self.rect.width:
                self.direction = "left"
        elif self.direction == "up":
            self.rect.y -= self.speed
            if self.rect.y < 0:
                self.direction = "down"
        elif self.direction == "down":
            self.rect.y += self.speed
            if self.rect.y > SCREEN_HEIGHT - self.rect.height:
                self.direction = "up"

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = bullet_image
        self.image = pygame.transform.scale(bullet_image, (30, 15)) 
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 6

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()

    def restart():
        global killed_tanks
        killed_tanks = 0
        all_sprites = pygame.sprite.Group()
        enemy_tanks = pygame.sprite.Group()
        bullets = pygame.sprite.Group()

    
        player = Tank(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        all_sprites.add(player)

        for _ in range(5):
            enemy = EnemyTank()
            enemy_tanks.add(enemy)
            all_sprites.add(enemy)

    

    



def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    all_sprites = pygame.sprite.Group()
    player = Tank(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    all_sprites.add(player)

    enemy_tanks = pygame.sprite.Group()
    for _ in range(10):
        enemy = EnemyTank()
        enemy_tanks.add(enemy)
        all_sprites.add(enemy)


    bullets = pygame.sprite.Group()  

    clock = pygame.time.Clock()
    running = True
    while running:
        # Обробка подій
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                Restart()

        # Обробка стрільби
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            if len(bullets) < 15: 
                bullet = Bullet(player.rect.centerx, player.rect.top)
                bullets.add(bullet)
                all_sprites.add(bullet)
                shoot_sound.play()
            else:
                pygame.time.wait(1000)  # Перезарядка 
        all_sprites.update()

        # Відображення
        screen.blit(background_image, (0, 0))  #  фон
        all_sprites.draw(screen)

        # зіткнення снаряда з ворожим танком
        hits = pygame.sprite.groupcollide(enemy_tanks, bullets, True, True)
        for hit in hits:
            global killed_tanks
            killed_tanks += 1

        # Перевірка зіткнення гравця з ворожим танком
        hits = pygame.sprite.spritecollide(player, enemy_tanks, True)
        if hits:
            text = font.render("Lose", True, WHITE)
            screen.blit(text, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2))
            pygame.display.flip()
            pygame.time.wait(2000)
            running = False

        # рахунок
        font = pygame.font.Font(None, 36)
        text = font.render("Killed Tanks: " + str(killed_tanks), True, WHITE)
        screen.blit(text, (10, 10))

        #RESTART
        restart_text = font.render("RESTART (Press R)", True, WHITE)
        screen.blit(restart_text, (10, SCREEN_HEIGHT - 40))



        if len(enemy_tanks) == 0:
            text = font.render("Win", True, WHITE)
            screen.blit(text, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2))
            pygame.display.flip()
            pygame.time.wait(2000)
            running = False

        if not player.alive():
            text = font.render("Lose", True, WHITE)
            screen.blit(text, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2))
            pygame.display.flip()
            pygame.time.wait(2000)
            running = False

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

