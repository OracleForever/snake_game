import pygame
import random

class Point:
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def copy(self):
        return Point(row=self.row, col=self.col)

#initialization
pygame.init()

#display
width = 600
height = 600
score = 0

#grid
ROW = 30
COL = 30

size = (width, height)
window = pygame.display.set_mode(size)
pygame.display.set_caption('Snake Game') #title
bg_color = (112, 128, 144)

#Define coordinates
snake_head = Point(row = int(ROW/2), col = int(COL/2))
head_color = (0, 0, 205)

snake_body = [
    Point(row=snake_head.row, col=snake_head.col+1),
    Point(row=snake_head.row, col=snake_head.col+2),
]

#generate food
def generate_food():
    while True:
        pos=Point(row = random.randint(0, ROW-1), col = random.randint(0, COL-1))
        on_body = False
        # if on the body
        if snake_head.row == pos.row and snake_head.col == pos.col:
            on_body = True
        #snake_body
        for body in snake_body:
            if body.row == pos.row and body.col == pos.col:
                on_body = True
                break
        if not on_body:
            break
    return pos

body_color = (0, 205, 0)
food = generate_food()
food_color = (255, 218, 185)

#direct: left, right, up, down
direct = 'left'

#position of snake
def rect(point, color):
    cell_w = width/COL
    cell_h = height/ROW
    left = point.col * cell_w
    top = point.row * cell_h
    pygame.draw.rect(
        window, color,
        (left, top, cell_w, cell_h)
    )

#Game Loop
running = True
clock = pygame.time.Clock()
while running:
    #handle events
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == 97 or event.key == 1073741904:
                if direct == 'up' or direct == 'down':
                    direct = 'left'
            elif event.key == 100 or event.key == 1073741903:
                if direct == 'up' or direct == 'down':
                    direct = 'right'
            elif event.key == 119 or event.key == 1073741906:
                if direct == 'left' or direct == 'right':
                    direct = 'up'
            elif event.key == 115 or event.key == 1073741905:
                if direct == 'left' or direct == 'right':
                    direct = 'down'

    #eat
    ate = (snake_head.row == food.row and snake_head.col == food.col)

    #refresh food
    if ate:
        food = generate_food()
        score += 1

    #move body
    #1. put snake_head into snake_body
    snake_body.insert(0, snake_head.copy())
    #2. delete the last of snake_body
    if not ate:
        snake_body.pop()

    #move
    if direct == 'left':
        snake_head.col -= 1
    elif direct == 'right':
        snake_head.col += 1
    elif direct == 'up':
        snake_head.row -= 1
    elif direct == 'down':
        snake_head.row += 1

    #check
    dead = False
    #1. hit wall
    if snake_head.row < 0 or snake_head.col < 0 or snake_head.row >= ROW or snake_head.col >= COL:
        dead = True
    #2. hit itself
    for body in snake_body:
        if snake_head.row == body.row and snake_head.col == body.col:
            dead = True
            break
    if dead:
        font = pygame.font.SysFont(None, 72)
        text = font.render('You Lose!', True, (255, 0, 0))
        window.blit(text, (width // 3, height // 2))
        pygame.display.flip()
        pygame.time.wait(2000)  #keep 2 seconds
        running = False
    #Render
    #background
    pygame.draw.rect(window, bg_color, (0, 0, width, height))

    # Scoreboard
    font = pygame.font.SysFont(None, 36)
    text = font.render(f'Score: {score}', True, (255, 255, 255))
    window.blit(text, (10, 10))

    #snake_head
    rect(snake_head, head_color)

    #snake_body
    for body in snake_body:
        rect(body, body_color)

    #food
    rect(food, food_color)

    pygame.display.flip()

    #Set the frame rate
    clock.tick(15)

