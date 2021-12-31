import pygame
import random
from Board import Board
from Snake import *

pygame.init()

WIDTH, HEIGHT = 800, 1000
FPS = 60
BOARD_IMAGE = pygame.image.load("Images/Background.png")

HEAD_UP = pygame.image.load("Images/snake_head_up.png")
HEAD_LEFT = pygame.image.load("Images/snake_head_left.png")
HEAD_DOWN = pygame.image.load("Images/snake_head_down.png")
HEAD_RIGHT = pygame.image.load("Images/snake_head_right.png")

BODY_VERTICAL = pygame.image.load("Images/snake_vertical.png")
BODY_HORIZONTAL = pygame.image.load("Images/snake_horizontal.png")
BODY_IMG = pygame.image.load("Images/snake_body.png")

APPLE_IMG = pygame.image.load("Images/apple.png")


class Apple:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, win):
        win.blit(APPLE_IMG, (self.x, self.y))


def is_valid_pos(apple_x, apple_y, snake_body, snake_head):
    if apple_x == snake_head.x and apple_y == snake_head.y:
        return False

    for snake in snake_body:
        if apple_x == snake.x and apple_y == snake.y:
            return False
    return True


def place_apple(snake_body, snake_head):
    row = [i for i in range(WIDTH) if i % 40 == 0]
    col = [i for i in range(HEIGHT) if i % 40 == 0]

    row_pos = random.choice(row)
    col_pos = random.choice(col)

    while not is_valid_pos(row_pos, col_pos, snake_body, snake_head):
        row_pos = random.choice(row)
        col_pos = random.choice(col)

    return Apple(row_pos, col_pos)


def redraw_gamewindow(win, snake_body, snake_head, board, apple):
    board.draw(win)

    snake_head.draw(win, snake_body)

    apple.draw(win)

    pygame.display.update()


def main():
    run = True
    clock = pygame.time.Clock()

    board = Board(40, 50, BOARD_IMAGE)
    snake_body = [SnakeBody(80, 400, "up", BODY_HORIZONTAL, BODY_VERTICAL, BODY_IMG),
                  SnakeBody(40, 400, "up", BODY_HORIZONTAL, BODY_VERTICAL, BODY_IMG)]
    snake_head = SnakeHead(120, 400, "down", HEAD_UP, HEAD_LEFT, HEAD_DOWN, HEAD_RIGHT)
    apple = place_apple(snake_body, snake_head)

    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake")

    loop = 0

    while run:
        loop += 1
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # controlling the snake
        x = snake_head.x // 40
        y = snake_head.y // 40

        #print(x)
        if y == 0 and x > 0:
            snake_head.facing = "left"
        elif x == 0 and y < HEIGHT // 40:
            snake_head.facing = "down"
        elif x == WIDTH // 40:
            snake_head.facing = "up"

        elif x % 2 != 0 and y == 1:
            snake_head.facing = "right"
        elif x % 2 == 0 and y == HEIGHT // 40:
            snake_head.facing = "right"

        elif x % 2 == 0:
            snake_head.facing = "down"

        elif x % 2 != 0:
            snake_head.facing = "up"

        # apple collision
        if snake_head.x == apple.x and snake_head.y == apple.y:
            apple = place_apple(snake_body, snake_head)
            # add snake body
            last_snake = snake_body[len(snake_body) - 1]
            facing = last_snake.facing
            if facing == "up":
                snake_body.append(
                    SnakeBody(last_snake.x, last_snake.y + 40, "up", BODY_HORIZONTAL, BODY_VERTICAL, BODY_IMG))
            elif facing == "left":
                snake_body.append(
                    SnakeBody(last_snake.x + 40, last_snake.y, "left", BODY_HORIZONTAL, BODY_VERTICAL, BODY_IMG))
            elif facing == "down":
                snake_body.append(
                    SnakeBody(last_snake.x, last_snake.y - 40, "down", BODY_HORIZONTAL, BODY_VERTICAL, BODY_IMG))
            elif facing == "right":
                snake_body.append(
                    SnakeBody(last_snake.x - 40, last_snake.y, "right", BODY_HORIZONTAL, BODY_VERTICAL, BODY_IMG))

        redraw_gamewindow(WIN, snake_body, snake_head, board, apple)

        if loop % 1 == 0:
            snake_head.move(snake_body)
            loop = 0

        if snake_head.collide(WIDTH, HEIGHT, snake_body):
            run = False

    pygame.quit()


main()
