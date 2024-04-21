
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

class Enemy(GameSprite):
    direction = "left"
    def update(self,x1,x2):
        if self.direction == "left":
            self.rect.x -= self.speed
        elif self.direction == "right":
             self.rect.x += self.speed
        
        if self.rect.x <= x1:
            self.direction = "right"
        elif self.rect.x >= x2:
            self.direction = "left"

    
class Wall(pygame.sprite.Sprite):
    def __init__(self, coords:tuple[int,int], size:tuple[int,int], color:tuple[int,int,int]):
        self.rect = pygame.rect.Rect(coords,size)
        self.color = color
    def draw_wall(self):
        pygame.draw.rect(window, self.color,self.rect)

   

    
        
        
        
        

player = Player("hero.png",(20,HEIGHT-70),5)
enemy = Enemy("cyborg.png",(WIDTH-100, HEIGHT/2),5)
gold = GameSprite("treasure.png",(WIDTH-40,HEIGHT-40),0)

walls = [
    Wall((10,10), (WIDTH-100,10), (255,0,0)),
    Wall((10,10), (10,HEIGHT-150),(255,0,0)),
    Wall((10,680), (WIDTH-40,10),(255,0,0)),
    Wall((10,400), (WIDTH-1000,10),(255,0,0)),
    Wall((200,400), (10,HEIGHT-550),(255,0,0)),
    Wall((200,550), (WIDTH-1000,10),(255,0,0)),
    Wall((200,450), (WIDTH-1000,10),(255,0,0)),
    Wall((200,400), (10,HEIGHT-550),(255,0,0)),
]

pygame.font.init()
font = pygame.font.Font(None, 70)
text_win = font.render("YOU WON",True,(255,215,0))
text_lose = font.render("YOU LOSE",True,(255,0,0))

money_sound = pygame.mixer.Sound("money.ogg")
kick_sound = pygame.mixer.Sound("Kick.ogg")

game_over = False
finish = False
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
    if not finish: 
        window.blit(background,(0,0))
        player.update()
        player.reset()
        enemy.update(WIDTH/2,WIDTH)
        enemy.reset()
        gold.reset()
        for w in walls:
            w.draw_wall()

        if pygame.sprite.collide_rect(player,gold):
            finish = True
            window.blit(text_win, (WIDTH/2-100,HEIGHT/2))
            money_sound.play()



        #перевіряє чи стикається гравець хоча б з однією стіною
        wall_collision = any([pygame.sprite.collide_rect(player,w) for w in walls])

        if pygame.sprite.collide_rect(player,enemy) or wall_collision:
            finish = True
            window.blit(text_lose, (WIDTH/2-100,HEIGHT/2))
            kick_sound.play()
    pygame.display.update()
    clock.tick(FPS)


