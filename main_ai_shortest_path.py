import pygame
import random
from Board import Board
from Snake import *

pygame.init()

WIDTH, HEIGHT = 800, 1000
FPS = 30

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

BOARD_IMAGE = pygame.image.load("Images/Background.png")

HEAD_UP = pygame.image.load("Images/snake_head_up.png")
HEAD_LEFT = pygame.image.load("Images/snake_head_left.png")
HEAD_DOWN = pygame.image.load("Images/snake_head_down.png")
HEAD_RIGHT = pygame.image.load("Images/snake_head_right.png")

BODY_VERTICAL = pygame.image.load("Images/snake_vertical.png")
BODY_HORIZONTAL = pygame.image.load("Images/snake_horizontal.png")
BODY_IMG = pygame.image.load("Images/snake_body.png")


APPLE_IMG = pygame.image.load("Images/apple.png")


def get_neighbors(matrix, pos):
    """
    :param matrix: the playing field
    :param pos: the position to get the neighbors from
    :return: returns all the neighbors of a position without the diagonal neighbors
    """
    row = pos[0]
    col = pos[1]

    neighbors = []

    if row != 0:
        neighbors.append((row-1, col))
    if row != len(matrix) - 1:
        neighbors.append((row + 1, col))
    if col != 0:
        neighbors.append((row, col - 1))
    if col != len(matrix[0]) - 1:
        neighbors.append((row, col + 1))

    return neighbors


def solve(board, s, rows, cols, n):
    r = s[0]
    c = s[1]

    q = [s]
    visited = []
    for _ in range(rows):
        visited.append([False] * cols)

    visited[r][c] = True

    prev = [None] * n

    while len(q) > 0:
        node = q[0]
        q.pop(0)

        neighbors = get_neighbors(board, node)

        for neighbor in neighbors:
            r_n = neighbor[0]
            c_n = neighbor[1]
            if not visited[r_n][c_n]:
                q.append(neighbor)
                visited[r_n][c_n] = True
                prev[r_n * cols + c_n] = node

    return prev


def reconstruct_path(s, e, prev, cols):
    path = []

    at_r = e[0]
    at_c = e[1]
    at = e
    prev_pos = at_r * cols + at_c

    while prev[prev_pos] is not None:
        path.append(at)

        at_r = prev[prev_pos][0]
        at_c = prev[prev_pos][1]
        at = prev[prev_pos]
        prev_pos = at_r * cols + at_c

    path.append(at)
    path.reverse()

    if path[0] == s:
        return path
    return []


def bfs(board, s, e):
    rows = len(board)
    cols = len(board[0])

    n = rows * cols

    prev = solve(board, s, rows, cols, n)

    return reconstruct_path(s, e, prev, cols)


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


def redraw_game_window(win, snake_body, snake_head, board, apple, path):
    board.draw(win)

    snake_head.draw(win, snake_body)

    apple.draw(win)

    for pair in path[:-1]:
        row = pair[1] * 40
        col = pair[0] * 40

        pygame.draw.rect(win, (150, 20, 250), (row, col, 40, 40))

    pygame.display.update()


def main():
    run = True
    clock = pygame.time.Clock()

    board = Board(20, 25, BOARD_IMAGE)
    snake_body = [SnakeBody(80, 400, "up", BODY_HORIZONTAL, BODY_VERTICAL, BODY_IMG),
                  SnakeBody(40, 400, "up", BODY_HORIZONTAL, BODY_VERTICAL, BODY_IMG)]
    snake_head = SnakeHead(120, 400, "right", HEAD_UP, HEAD_LEFT, HEAD_DOWN, HEAD_RIGHT)
    apple = place_apple(snake_body, snake_head)

    loop = 0

    board.apple = (apple.y // 40, apple.x // 40)
    board.update(snake_head, snake_body)

    # bfs to find the best path

    path = bfs(board.board, (snake_head.y // 40, snake_head.x // 40), (apple.y // 40, apple.x // 40))
    path.pop(0)

    while run:
        loop += 1
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # apple collision
        if snake_head.x == apple.x and snake_head.y == apple.y:
            board.construct_board()

            apple = place_apple(snake_body, snake_head)

            board.apple = (apple.y // 40, apple.x // 40)
            board.update(snake_head, snake_body)

            # bfs to find the best path

            path = bfs(board.board, (snake_head.y // 40, snake_head.x // 40), (apple.y // 40, apple.x // 40))
            path.pop(0)
            # print(path, (apple.y // 40, apple.x // 40))

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

        redraw_game_window(WIN, snake_body, snake_head, board, apple, path)

        if loop % 5 == 0:

            # controlling the snake
            # if path is emtpy --> snake is dead
            if not path:
                run = False

            old_r = snake_head.y // 40
            old_c = snake_head.x // 40

            new_r = path[0][0]
            new_c = path[0][1]

            if new_r > old_r:
                snake_head.facing = "down"

            elif new_r < old_r:
                snake_head.facing = "up"

            elif new_c > old_c:
                snake_head.facing = "right"

            elif new_c < old_c:
                snake_head.facing = "left"

            path.pop(0)

            snake_head.move(snake_body)
            loop = 0

        if snake_head.collide(WIDTH, HEIGHT, snake_body):
            run = False

    pygame.quit()


main()
