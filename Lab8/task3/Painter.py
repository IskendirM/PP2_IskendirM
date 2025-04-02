import pygame

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()
    
    radius = 15
    mode = 'blue'
    drawing_mode = 'drawing' 
    points = []
    shapes = []  
    rect_start = None
    circle_start = None

    while True:
        pressed = pygame.key.get_pressed()
        alt_held = pressed[pygame.K_LALT] or pressed[pygame.K_RALT]
        ctrl_held = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and ctrl_held:
                    return
                if event.key == pygame.K_F4 and alt_held:
                    return
                if event.key == pygame.K_ESCAPE:
                    return

                #color change
                if event.key == pygame.K_r:
                    mode = 'red'
                    drawing_mode = 'drawing'
                elif event.key == pygame.K_g:
                    mode = 'green'
                    drawing_mode = 'drawing'
                elif event.key == pygame.K_b:
                    mode = 'blue'
                    drawing_mode = 'drawing'
                elif event.key == pygame.K_e:
                    drawing_mode = 'eraser'  

                #choose shape
                elif event.key == pygame.K_t:
                    drawing_mode = 'rect'
                    rect_start = None
                elif event.key == pygame.K_c:
                    drawing_mode = 'circle'
                    circle_start = None

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  
                    if drawing_mode == 'drawing' or drawing_mode == 'eraser':
                        radius = min(200, radius + 1)
                    elif drawing_mode == 'rect':
                        rect_start = event.pos
                    elif drawing_mode == 'circle':
                        circle_start = event.pos

                elif event.button == 3:
                    if drawing_mode == 'drawing' or drawing_mode == 'eraser':
                        radius = max(1, radius - 1)
                    elif drawing_mode == 'rect' and rect_start:
                        shapes.append(("rect", rect_start, pygame.mouse.get_pos(), mode))
                        rect_start = None
                    elif drawing_mode == 'circle' and circle_start:
                        shapes.append(("circle", circle_start, pygame.mouse.get_pos(), mode))
                        circle_start = None
                    drawing_mode = 'drawing' 

            if event.type == pygame.MOUSEMOTION:
                if drawing_mode == 'drawing' or drawing_mode == 'eraser':
                    position = event.pos
                    points.append((position, mode if drawing_mode == 'drawing' else 'eraser'))
                    points = points[-256:]

        screen.fill((0, 0, 0))

        #draw with 
        for i in range(len(points) - 1):
            drawLineBetween(screen, i, points[i][0], points[i + 1][0], radius, points[i][1])

        for shape in shapes:
            if shape[0] == "rect":
                drawRectangle(screen, shape[1], shape[2], shape[3])
            elif shape[0] == "circle":
                drawCircle(screen, shape[1], shape[2], shape[3])

        #draw rectangle
        if drawing_mode == 'rect' and rect_start:
            mouse_pos = pygame.mouse.get_pos()
            pygame.draw.rect(screen, get_color(mode), (*rect_start, mouse_pos[0] - rect_start[0], mouse_pos[1] - rect_start[1]), 2)

        #draw cicle
        if drawing_mode == 'circle' and circle_start:
            mouse_pos = pygame.mouse.get_pos()
            radius = int(((mouse_pos[0] - circle_start[0]) ** 2 + (mouse_pos[1] - circle_start[1]) ** 2) ** 0.5)
            pygame.draw.circle(screen, get_color(mode), circle_start, radius, 2)

        pygame.display.flip()
        clock.tick(60)


def drawLineBetween(screen, index, start, end, width, color_mode):
    c1 = max(0, min(255, 2 * index - 256))
    c2 = max(0, min(255, 2 * index))

    if color_mode == 'blue':
        color = (c1, c1, c2)
    elif color_mode == 'red':
        color = (c2, c1, c1)
    elif color_mode == 'green':
        color = (c1, c2, c1)
    elif color_mode == 'eraser':
        color = (0, 0, 0)

    dx = start[0] - end[0]
    dy = start[1] - end[1]
    iterations = max(abs(dx), abs(dy))

    for i in range(iterations):
        progress = 1.0 * i / iterations
        aprogress = 1 - progress
        x = int(aprogress * start[0] + progress * end[0])
        y = int(aprogress * start[1] + progress * end[1])
        pygame.draw.circle(screen, color, (x, y), width)


def drawRectangle(screen, start, end, mode):
    pygame.draw.rect(screen, get_color(mode), (*start, end[0] - start[0], end[1] - start[1]), 2)


def drawCircle(screen, start, end, mode):
    radius = int(((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2) ** 0.5)
    pygame.draw.circle(screen, get_color(mode), start, radius, 2)


def get_color(mode):
    if mode == 'blue':
        return (0, 0, 255)
    elif mode == 'red':
        return (255, 0, 0)
    elif mode == 'green':
        return (0, 255, 0)
    return (255, 255, 255)


main()
