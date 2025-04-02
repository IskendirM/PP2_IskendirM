#File must be executed in dir where placed task 
#in the terminal use cd .\Lab8\task1
#then you can start game

import pygame, sys
from pygame.locals import *
import random, time


pygame.init()

 
FPS = 60
TickController = pygame.time.Clock() #to control ticks in the game, it's depend as reverse qudradic rule

BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

SPEED = 5
PLAYER_SPEED = 5
SCORE = 100
COIN = 0



font = pygame.font.SysFont("Verdana", 60) #main font
font_small = pygame.font.SysFont("Verdana", 20)

game_over = font.render("Game Over", True, BLACK) #massage "Game over"
you_win = font.render("You Win", True, BLACK) #masssage "You win"

background = pygame.image.load("AnimatedStreet.png")


SCREEN = pygame.display.set_mode((400,600))
SCREEN.fill(WHITE)
pygame.display.set_caption("Car Crush")


class Enemy(pygame.sprite.Sprite):
      def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Enemy.png") #if file don't execute send full path to this png file
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40,SCREEN_WIDTH-40), 0)

      def move(self):
        global SCORE
        self.rect.move_ip(0,SPEED)

        if (self.rect.bottom > 600):
            SCORE -= 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)


class Player(pygame.sprite.Sprite):
    global PLAYER_SPEED
    
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)
       
   

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        

        if self.rect.left > 0:
              if pressed_keys[K_LEFT]:
                  self.rect.move_ip(-(PLAYER_SPEED), 0)
        if self.rect.right < SCREEN_WIDTH:        
              if pressed_keys[K_RIGHT]:
                  self.rect.move_ip(PLAYER_SPEED, 0)


class BuffCoin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("BuffCoin2.png")
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40,SCREEN_WIDTH-40), 0)
        
    def move(self):
        global SCORE
        global SPEED

        self.rect.move_ip(0, 3)
        if(self.rect.bottom > 600):
            self.rect.top = 0
            self.rect.center = (random.randint(50, SCREEN_WIDTH - 40), 0)
    
    def spawn(self):
        self.rect.top = 0
        self.rect.center = (random.randint(50, SCREEN_WIDTH - 40), 0)

    def getBuff(self):
        global SPEED
       
        if SPEED > 10:
            SPEED -= 5
            self.rect.top = 0
            self.rect.center = (random.randint(50, SCREEN_WIDTH - 40), 0)                  


class TextDisplayer():
    """class for diplsaying text"""

    def __init__(self):
        super().__init__()

    def Print(self, text, text_position: tuple, text_color: tuple = BLACK, bg_color:tuple = WHITE):
        SCREEN.fill(bg_color)
        SCREEN.blit(font.render(text, True, text_color),  text_position)


        

Player = Player()
car_enemy = Enemy()

text = TextDisplayer()
buff_coin = BuffCoin()
buffers_sprites = pygame.sprite.Group()
buffers_sprites.add(buff_coin)


enemies = pygame.sprite.Group()
enemies.add(car_enemy)

all_sprites = pygame.sprite.Group()
all_sprites.add(Player)
all_sprites.add(car_enemy)


INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 3000)


while True:
    isBuffed = False

    for event in pygame.event.get():
        if event.type == INC_SPEED:
              SPEED += 0.5      
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()


    SCREEN.blit(background, (0,0))
    scores = font_small.render(f"CAR: {str(SCORE)}", True, BLACK)
    coin = font_small.render(f"COIN: {str(COIN)}", True, BLACK)
    SCREEN.blit(scores, (10,10))
    SCREEN.blit(coin, (SCREEN_WIDTH - 100,10))

    if random.randint(1, 50) == 1:
       all_sprites.add(buff_coin)

    for entity in all_sprites:
        entity.move()
        SCREEN.blit(entity.image, entity.rect)

    if pygame.sprite.spritecollideany(Player, buffers_sprites) and not isBuffed:
        #check colaidor with coins
        buff_coin.getBuff()
        isBuffed = False
        COIN += 1
        buff_coin.spawn()    

    if pygame.sprite.spritecollideany(Player, enemies):
        #check crash with another car
        time.sleep(1)
                   
        SCREEN.fill(RED)
        SCREEN.blit(game_over, (30,250))
          
        pygame.display.update()
        for entity in all_sprites:
            entity.kill() 
        time.sleep(2)
        pygame.quit()
        sys.exit()
   
   
    if SCORE == 0:
        time.sleep(1)
        text.Print("YOU WIN", (50, 250), BLACK, GREEN)
        pygame.display.update()
        for entity in all_sprites:
            entity.kill() 
            
        time.sleep(2)
        pygame.quit()
        sys.exit()    
        
    pygame.display.update()
    TickController.tick(FPS)
