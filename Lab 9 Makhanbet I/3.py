import pygame
import math

#initalization
pygame.init()
font = pygame.font.Font(None , 36)
remove_text = font.render("REMOVE", True, (255 , 255 , 255))
remove_rect = pygame.Rect(800 , 5 , 150 , 50)

# colors
WHITE = (255, 255, 255)
BLUE = (0,0,255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GRAY = (140,140,140)
DARK_GRAY = (100,100,100)

# display
screen_l = 1000
screen_h = 700
screen = pygame.display.set_mode((screen_l , screen_h))
pygame.display.set_caption("Paint")

#draw and running 
running = True
drawing = False

#sellect instruments
brush_selected = True  # Флаг выбора кисти
brush_radius = 5
circle_selected = False
rect_selected = False
tri_selected = False
rhm_sellected = False
a_sellected = False


#load images
img_brush = pygame.transform.scale(pygame.image.load("lab8/img/brush.png"), (50, 50))
rect_brush = pygame.Rect(425, 5, 50, 50)

img_eraser = pygame.transform.scale(pygame.image.load("lab8/img/eraser.png"), (50, 50))
rect_eraser = pygame.Rect(500, 5, 50, 50)

img_circle = pygame.transform.scale(pygame.image.load("lab8/img/circle.png"), (50, 50))
rect_circle = pygame.Rect(600 , 5 , 50 , 50)
c_top_l = None
c_bottom_r = None

img_rect = pygame.transform.scale(pygame.image.load("lab8/img/rect.png"), (50, 50))
rect_rect = pygame.Rect(700, 5, 50, 50)
r_top_l = None
r_bottom_r = None

img_tri = pygame.transform.scale(pygame.image.load("lab8/img/triangle.png") , (50 , 50))
rect_tri = pygame.Rect(600 , 75 , 50 , 50)
t_top_l = None
t_bottom_r = None

img_rhm = pygame.transform.scale(pygame.image.load("lab8/img/rhombus.png") , (50 , 50))
rect_rhm = pygame.Rect(700 , 75 , 50 , 50)
rhm_top_l = None
rhm_bottom_r = None

img_a = pygame.transform.scale(pygame.image.load("lab8/img/a.png") , (50 , 50))
rect_a = pygame.Rect(800 , 75 , 50 , 50)
a_top_l = None
a_bottom_r = None



#rectangles of shapes
img_color = pygame.transform.scale(pygame.image.load("lab8/img/color.png"), (50, 50))
red_rect = pygame.Rect(80 , 5 , 50 , 50)
blue_rect = pygame.Rect(135 , 5 , 50 , 50)
green_rect = pygame.Rect(190 , 5 , 50 , 50)
black_rect = pygame.Rect(245 , 5 , 50 , 50)
white_rect = pygame.Rect(300 , 5 , 50 , 50)
darkgray_rect = pygame.Rect(355 , 5 , 50 , 50)


#gray icon under instruments
icon = pygame.Rect(0 ,0 , screen_l , 130)

#color of drawing
current_color = BLACK

#we are drawing with lines
last_pos = None

#paper
screen.fill(WHITE)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #sellecting color
        if event.type == pygame.MOUSEBUTTONDOWN:
            if red_rect.collidepoint(event.pos):
                current_color = RED
            elif blue_rect.collidepoint(event.pos):
                current_color = BLUE
            elif green_rect.collidepoint(event.pos):
                current_color = GREEN
            elif black_rect.collidepoint(event.pos):
                current_color = BLACK
            elif darkgray_rect.collidepoint(event.pos):
                current_color = DARK_GRAY
            elif white_rect.collidepoint(event.pos):
                current_color = WHITE

            #sellect eraser
            elif rect_eraser.collidepoint(event.pos):
                current_color = WHITE
                brush_selected = True
                circle_selected = False
                rect_selected = False
                a_sellected = False
            #remover
            elif remove_rect.collidepoint(event.pos):
                screen.fill(WHITE)

            #sellecting instruments
            if rect_brush.collidepoint(event.pos):
                brush_selected = True
                circle_selected = False
                rect_selected = False
                brush_radius = 5
                tri_selected = False
                rhm_sellected = False
                a_sellected = False
            elif rect_circle.collidepoint(event.pos):
                brush_selected = False
                circle_selected = True
                rect_selected = False
                tri_selected = False
                rhm_sellected = False
                a_sellected = False
            elif rect_rect.collidepoint(event.pos):
                brush_selected = False
                circle_selected = False
                rect_selected = True
                tri_selected = False
                rhm_sellected = False
                a_sellected = False
            elif rect_tri.collidepoint(event.pos):
                brush_selected = False
                circle_selected = False
                rect_selected = False
                tri_selected = True
                rhm_sellected = False
                a_sellected = False
            elif rect_rhm.collidepoint(event.pos):
                brush_selected = False
                circle_selected = False
                rect_selected = False
                tri_selected = False
                rhm_sellected = True
                a_sellected = False
            elif rect_a.collidepoint(event.pos):
                brush_selected = False
                circle_selected = False
                rect_selected = False
                tri_selected = False
                rhm_sellected = False
                a_sellected = True


            elif brush_selected:
                drawing = True
                last_pos = event.pos
            elif circle_selected:
                c_top_l = event.pos
                drawing = True
            elif rect_selected:
                r_top_l = event.pos
                drawing = True
            elif tri_selected:
                t_top_l = event.pos
                drawing = True
            elif rhm_sellected:
                rhm_top_l = event.pos
                drawing = True
            elif a_sellected:
                a_top_l  = event.pos
                drawing = True


        if event.type == pygame.MOUSEBUTTONUP:
            if brush_selected:
                drawing = False
                last_pos = None

            elif circle_selected and drawing:
                c_bottom_r = event.pos
                drawing = False
                dx = c_bottom_r[0] - c_top_l[0]
                dy = c_bottom_r[1] - c_top_l[1]
                radius = int(math.hypot(dx, dy))
                pygame.draw.circle(screen, current_color, c_top_l, radius)

            elif rect_selected and drawing:
                r_bottom_r = event.pos
                drawing = False
                x = min(r_top_l[0], r_bottom_r[0])
                y = min(r_top_l[1], r_bottom_r[1])
                width = abs(r_bottom_r[0] - r_top_l[0])
                height = abs(r_bottom_r[1] - r_top_l[1])
                pygame.draw.rect(screen, current_color, (x, y, width, height))

            elif tri_selected and drawing:
                t_bottom_r = event.pos
                drawing = False
                x1, y1 = t_top_l
                x2, y2 = t_bottom_r
                point1 = (x1, y1)
                point2 = (x2, y1)  
                point3 = (x1 + (x2 - x1) // 2, y2)  
                pygame.draw.polygon(screen, current_color, [point1, point2, point3])

            elif rhm_sellected and drawing:
                rhm_bottom_r = event.pos
                drawing = False
                x1, y1 = rhm_top_l
                x2, y2 = rhm_bottom_r
                point1 = ((x2-x1)/2 + x1 , y1)
                point2 = (x2 , (y2-y1)/2 + y1)
                point3 = ((x2-x1)/2 + x1 , y2)
                point4 = (x1 , (y2-y1)/2 + y1)
                pygame.draw.polygon(screen , current_color , [point1 , point2 , point3 , point4])
            
            elif a_sellected and drawing:
                a_bottom_r = event.pos
                drawing = False
                x1, y1 = a_top_l
                x2, y2 = a_bottom_r
                point1 = (x1, y1)
                point2 = (x2, y2)  
                point3 = (x1 , y2) 
                pygame.draw.polygon(screen, current_color, [point1, point2, point3])
                




        if event.type == pygame.MOUSEMOTION and drawing and brush_selected:
            if last_pos:
                pygame.draw.line(screen, current_color, last_pos, event.pos, brush_radius)
            last_pos = event.pos

    pygame.draw.rect(screen , GRAY , icon)

    screen.blit(img_color , (5 , 5))
    pygame.draw.rect(screen , RED , red_rect)
    pygame.draw.rect(screen , BLUE , blue_rect)
    pygame.draw.rect(screen , GREEN , green_rect)
    pygame.draw.rect(screen , BLACK , black_rect)
    pygame.draw.rect(screen , WHITE , white_rect)
    pygame.draw.rect(screen , DARK_GRAY , darkgray_rect)

    screen.blit(img_brush , (425, 5))
    screen.blit(img_eraser , (500, 5))
    screen.blit(img_circle , (600, 5))
    screen.blit(img_rect , (700, 5))
    screen.blit(img_tri , (600, 75))
    screen.blit(img_rhm , (700 , 75))
    screen.blit(img_a , (800  ,75))

    pygame.draw.rect(screen , DARK_GRAY , remove_rect)
    screen.blit(remove_text , (820 , 15 , 150 , 50))

    pygame.display.update()
