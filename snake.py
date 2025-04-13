import pygame
import random
import sys

import insert
import update
import query


# инициализация
pygame.init()
pygame.mixer.init()

# окно параметры
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game Demo")
clock = pygame.time.Clock()

# шрифт
font = pygame.font.Font(None, 30)

# Input

input_box = pygame.Rect(100, 80, 400, 50)
color_inactive = pygame.Color('lightskyblue3')
color_active = pygame.Color('dodgerblue2')
color = color_inactive
active = False
text = ''

# базовыве цвета
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# параметры змейки
snake_pos = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50]]
snake_direction = "RIGHT"
change_to = snake_direction
speed = 15

# еда
food_pos = [random.randrange(1, (WIDTH // 10)) * 10, random.randrange(1, (HEIGHT // 10)) * 10]
food_spawn = True
food_weight = random.randint(1, 5)  # UPD: фича с весом еды

# параметры игры
game_score = 0
level = 1
foods_eaten = 0
isRunning = True
input_is_done = False

# параметры уровней
levels_data = {
    1: {
        "speed": 10,
        "walls": []
    },
    2: {
        "speed": 12,
        "walls": [[150, 150], [160, 150], [170, 150], [180, 150], [190, 150]]
    },
    3: {
        "speed": 15,
        "walls": [[250, 100], [260, 100], [270, 100], [280, 100], [290, 100],
                  [250, 110], [260, 110], [270, 110], [280, 110], [290, 110]]
    },
    4: {
        "speed": 18,
        "walls": [[350, 250], [360, 250], [370, 250], [380, 250], [390, 250],
                  [350, 260], [360, 260], [370, 260], [380, 260], [390, 260],
                  [350, 270], [360, 270], [370, 270], [380, 270], [390, 270]]
    },
    5: {
        "speed": 23,
        "walls": [[x, y] for x in range(100, 500, 10) for y in range(100, 200, 10)]
    }
}

# генерация еды
def generate_food():
    while True:
        food_pos = [random.randrange(1, (WIDTH // 10)) * 10, random.randrange(1, (HEIGHT // 10)) * 10]
        food_weight = random.randint(1, 5)  # UPD: параметр веса еды
        # чек не спавна на змейке
        if food_pos not in snake_body and food_pos not in current_walls:
            return food_pos, food_weight

# input shit
while not input_is_done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Если клик по input_box — активируем ввод
            if input_box.collidepoint(event.pos):
                active = not active
            else:
                active = False
            color = color_active if active else color_inactive

        if event.type == pygame.KEYDOWN:
            if active:
                if event.key == pygame.K_RETURN:
                    print("Введено:", text)
                    # Сохранение имени игрока в переменной
                    player_name = text
                    text = ''
                    input_is_done = True  # Завершить ввод текста
                    isRunning = True  # Начать игру
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode

    screen.fill((30, 30, 30))
    txt_surface = font.render(text, True, color)
    width = max(400, txt_surface.get_width()+10)
    input_box.w = width
    screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
    pygame.draw.rect(screen, color, input_box, 2)

    pygame.display.flip()
    clock.tick(30)

best_score_text = str(query.get_score_by_username(player_name))

# цикл игры
paused = False  # Initialize pause flag
while isRunning:
    current_walls = levels_data[level]["walls"] if level in levels_data else []

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            # управление
            if event.key == pygame.K_UP and snake_direction != "DOWN":
                change_to = "UP"
            if event.key == pygame.K_DOWN and snake_direction != "UP":
                change_to = "DOWN"
            if event.key == pygame.K_LEFT and snake_direction != "RIGHT":
                change_to = "LEFT"
            if event.key == pygame.K_RIGHT and snake_direction != "LEFT":
                change_to = "RIGHT"
            # Add pause toggle
            if event.key == pygame.K_SPACE:
                paused = not paused

    # Skip game logic if paused
    if paused:
        # Draw pause text
        pause_text = font.render("PAUSED", True, WHITE)
        pause_rect = pause_text.get_rect(center=(WIDTH/2, HEIGHT/2))
        screen.blit(pause_text, pause_rect)
        pygame.display.flip()
        continue

    # Rest of the game logic remains the same
    snake_direction = change_to

    if snake_direction == "UP":
        snake_pos[1] -= 10
    elif snake_direction == "DOWN":
        snake_pos[1] += 10
    elif snake_direction == "LEFT":
        snake_pos[0] -= 10
    elif snake_direction == "RIGHT":
        snake_pos[0] += 10

    snake_body.insert(0, list(snake_pos))

    if snake_pos == food_pos:
        food_spawn = False
        game_score += food_weight
        foods_eaten += 1
        if foods_eaten >= 3:
            if level < 5:
                level += 1
                if level in levels_data:
                    current_walls = levels_data[level]["walls"]
                else:
                    current_walls = []
                foods_eaten = 0
    else:
        snake_body.pop()

    if not food_spawn:
        food_pos, food_weight = generate_food()
        food_spawn = True

    if (snake_pos[0] < 0 or snake_pos[0] >= WIDTH or snake_pos[1] < 0 or snake_pos[1] >= HEIGHT) and player_name != "THAT_GUY":
        isRunning = False
    
    if snake_pos[0] < 0 or snake_pos[0] >= WIDTH or snake_pos[1] < 0 or snake_pos[1] >= HEIGHT and player_name == "THAT_GUY":
        snake_pos[0] = snake_pos[0] % WIDTH
        snake_pos[1] = snake_pos[1] % HEIGHT

    for block in snake_body[1:]:
        if snake_pos == block and player_name != "THAT_GUY": # "THAT_GUY" - это читер, который может убивать себя
            isRunning = False

    if snake_pos in current_walls and player_name != "THAT_GUY":  # Проверка на столкновение со стенами
        isRunning = False

    screen.fill(BLACK)
    for p in snake_body:
        pygame.draw.rect(screen, GREEN, pygame.Rect(p[0], p[1], 10, 10))
    pygame.draw.rect(screen, RED, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

    for wall in current_walls:
        pygame.draw.rect(screen, (100, 100, 100), pygame.Rect(wall[0], wall[1], 10, 10))

    game_score_text = font.render(f"Score: {game_score}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, WHITE)
    screen.blit(game_score_text, (20, 20))
    screen.blit(font.render(f"Player: {player_name}", True, WHITE), (20, 80))
    screen.blit(level_text, (20, 50))
    best_score_display = font.render(f"Best Score: {best_score_text}", True, WHITE)
    screen.blit(best_score_display, (20, 120))  # Отображение счёта игрока


    pygame.display.flip()
    clock.tick(levels_data[level]["speed"])

# гейм овер скрин и сохранение в БД
if query.get_score_by_username(player_name) is None:  # Проверка, существует ли игрок в БД
    try:
        insert.insert_player(player_name, game_score)  # Сохранение нового игрока в БД
    except Exception as e:
        print(f"Error inserting player into database: {e}")
else:
    if game_score > query.get_score_by_username(player_name):  # Если игрок уже есть в БД, обновляем его счёт
        try:
            update.update_score(player_name, game_score)  # Обновление в БД
        except Exception as e:
            print(f"Error updating player score in database: {e}")

game_over_text = font.render("GAME OVER", True, WHITE)
game_over_rectangle = game_over_text.get_rect()
game_over_rectangle.center = (WIDTH / 2, HEIGHT / 2)
screen.blit(game_over_text, game_over_rectangle)
pygame.display.update()
pygame.time.wait(3000)  # 3 секунды после чего игра закрывается
pygame.quit()

# TODO: добавить сохранение в БД ///  Сделано

# БД структура; snake -> Players -> username | score
