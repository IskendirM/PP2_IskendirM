import pygame
import random

pygame.init()

SCREEN_WIDTH = 300
SCREEN_HEIGHT = 300

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#Variables
score = 0
fruit_eaten = False
level = 0
snake_speed = 10

#generate fruit with random weight
def spawn_fruit():
    x = random.randrange(1, SCREEN_WIDTH // 10) * 10
    y = random.randrange(1, SCREEN_HEIGHT // 10) * 10
    weight = random.choice([5, 10])  #fruit weight
    return [[x, y], weight]

fruit = spawn_fruit()
fruit_timer = 10000  #fruit timer in milliseconds
fruit_spawn_time = pygame.time.get_ticks()

# Snake head and body
head_square = [100, 100]
squares = [
    [30, 100], 
    [40, 100], 
    [50, 100], 
    [60, 100],
    [70, 100], 
    [80, 100], 
    [90, 100], 
    [100, 100]
]

direction = "right"
next_dir = "right"

done = False

def game_over():
    global done
    font = pygame.font.SysFont("times new roman", 20)
    surface = font.render(f"Game Over, your score: {score}", True, (128, 128, 128))
    rect = surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(surface, (60, 120))
    pygame.display.update()
    pygame.time.delay(4000)
    done = True
    pygame.quit()

while not done:
    #handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        #handle key downs to control the snake
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                next_dir = "down"
            if event.key == pygame.K_UP:
                next_dir = "up"
            if event.key == pygame.K_LEFT:
                next_dir = "left"
            if event.key == pygame.K_RIGHT:
                next_dir = "right"

    #check if head meets body
    for square in squares[:-1]:
        if head_square == square:
            game_over()

    #check boundaries
    if head_square[0] < 0 or head_square[0] >= SCREEN_WIDTH or head_square[1] < 0 or head_square[1] >= SCREEN_HEIGHT:
        game_over()

    #update movement direction
    if next_dir == "right" and direction != "left":
        direction = "right"
    if next_dir == "up" and direction != "down":
        direction = "up"
    if next_dir == "left" and direction != "right":
        direction = "left"
    if next_dir == "down" and direction != "up":
        direction = "down"

    #snake movement
    if direction == "right":
        head_square[0] += snake_speed
    if direction == "left":
        head_square[0] -= snake_speed
    if direction == "up":
        head_square[1] -= snake_speed
    if direction == "down":
        head_square[1] += snake_speed

    #save old coordinates and update snake body
    new_square = list(head_square)
    squares.append(new_square)
    squares.pop(0)

    #check if snake eats fruit
    if head_square == fruit[0]:
        fruit_eaten = True
        score += fruit[1]

    #level logic with speed 
    if score >= 25:
        level = 1
        #snake_speed = 15
    if score >= 50:
        level = 2
        #snake_speed = 25
    if score >= 75:
        level = 3
        #snake_speed = 35

    #respawn fruit
    if fruit_eaten or pygame.time.get_ticks() - fruit_spawn_time > fruit_timer:
        fruit = spawn_fruit()
        fruit_spawn_time = pygame.time.get_ticks()
        fruit_eaten = False


    screen.fill((0, 0, 0))

    #display score and level
    font = pygame.font.SysFont("times new roman", 20)
    score_surface = font.render(f"Score: {score}", True, (128, 128, 128))
    level_display = font.render(f"Level: {level}", True, (128, 128, 128))
    screen.blit(score_surface, (10, 10))
    screen.blit(level_display, (220, 10))


    pygame.draw.circle(screen, (255, 0, 0), (fruit[0][0] + 5, fruit[0][1] + 5), 5)

    #draw snake
    for el in squares:
        pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(el[0], el[1], 10, 10))

    pygame.display.flip()
    pygame.time.delay(200)

pygame.quit()
