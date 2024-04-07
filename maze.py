from typing import Any
import pygame


WIDTH = 1200
HEIGHT = 700
SIZE  = (WIDTH,HEIGHT)


window = pygame.display.set_mode(SIZE)



background = pygame.transform.scale(
    pygame.image.load("background.jpg"),
    SIZE
)
FPS = 60
clock = pygame.time.Clock()
pygame.mixer.init()
pygame.mixer.music.load("jungles.ogg")
pygame.mixer.music.play()

class GameSprite(pygame.sprite.Sprite):
    def __init__(self,image,coords:tuple[int,int],speed): 
        super().__init__()
        self.image = pygame.transform.scale(
            pygame.image.load(image),
            (65,65)
        )
        self.rect = self.image.get_rect()
        self.rect.center = coords
        self.speed = speed

    def reset(self):
        window.blit(self.image,self.rect.topleft)


class Player(GameSprite):
    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_s] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed
        if keys[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_d] and self.rect.right < WIDTH:
            self.rect.x += self.speed
        
        
        
        

player = Player("hero.png",(20,HEIGHT-20),5)
enemy = GameSprite("cyborg.png",(WIDTH-100, HEIGHT/2),5)
gold = GameSprite("treasure.png",(WIDTH-40,HEIGHT-40),0)

game_over = False
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    window.blit(background,(0,0))
    player.update()
    player.reset()
    enemy.reset()
    gold.reset()

    pygame.display.update()
    clock.tick(FPS)


