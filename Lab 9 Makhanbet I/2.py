import pygame
from random import randrange
import sys

pygame.init()

# Экран
LENGTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((LENGTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

# Шрифты
font = pygame.font.Font(None, 30)

# Цвета
WHITE, GREEN, RED, BLACK = (255, 255, 255), (0, 255, 0), (255, 0, 0), (0, 0, 0)

# Настройки змейки
s_pos = [100, 50]
s_body = [[100, 50], [90, 50], [80, 50]]
s_dir = "RIGHT"
speed = 10

# Функция спавна еды
def spawn_food():
    while True:
        food = [randrange(0, LENGTH // 10) * 10, randrange(0, HEIGHT // 10) * 10]
        if food not in s_body:
            return food

f_pos = spawn_food()

# Функция спавна большой еды
def spawn_large_food():
    return [randrange(0, LENGTH // 10) * 10, randrange(0, HEIGHT // 10) * 10]




large_f_pos = None

# Очки
game_score = 0
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_w, pygame.K_UP) and s_dir != "DOWN":
                s_dir = "UP"
            elif event.key in (pygame.K_s, pygame.K_DOWN) and s_dir != "UP":
                s_dir = "DOWN"
            elif event.key in (pygame.K_a, pygame.K_LEFT) and s_dir != "RIGHT":
                s_dir = "LEFT"
            elif event.key in (pygame.K_d, pygame.K_RIGHT) and s_dir != "LEFT":
                s_dir = "RIGHT"
    
    # Движение змейки
    if s_dir == "UP":
        s_pos[1] -= 10
    elif s_dir == "DOWN":
        s_pos[1] += 10
    elif s_dir == "LEFT":
        s_pos[0] -= 10
    elif s_dir == "RIGHT":
        s_pos[0] += 10
    
    # Обновление тела змейки
    s_body.insert(0, list(s_pos))

    if s_pos == f_pos:
        game_score += 1
        f_pos = spawn_food()
        
    elif large_f_pos and s_pos == large_f_pos :
        game_score += 3
        large_f_pos = None

    else:
        s_body.pop()
    
    # Проверка столкновений
    if s_pos[0] < 0 or s_pos[0] >= LENGTH or s_pos[1] < 0 or s_pos[1] >= HEIGHT or s_pos in s_body[1:]:
        running = False
    
    # Отрисовка экрана
    screen.fill(GREEN)
    for part in s_body:
        pygame.draw.rect(screen, BLACK, pygame.Rect(part[0], part[1], 10, 10))
    pygame.draw.rect(screen, RED, pygame.Rect(f_pos[0], f_pos[1], 10, 10))
    if large_f_pos:
        pygame.draw.rect(screen, RED, pygame.Rect(large_f_pos[0], large_f_pos[1], 20, 20))
    
    score_text = font.render(f"Your score: {game_score}", True, WHITE)
    screen.blit(score_text, (20, 20))
    pygame.display.update()
    clock.tick(speed)

# Экран Game Over
screen.fill(BLACK)
game_over_text = font.render("GAME OVER", True, WHITE)
screen.blit(game_over_text, (LENGTH // 2 - 50, HEIGHT // 2))
pygame.display.update()
pygame.time.wait(3000)
pygame.quit()
