import pygame


class Board:
    def __init__(self, width, height, board_img):
        self.width = width
        self.height = height
        self.board_img = board_img

        self.board = []
        self.construct_board()
        self.apple = None

    def __repr__(self):
        for row in self.board:
            print(row)
        print("-------------------------------------------")

    def construct_board(self):
        self.board = []
        for i in range(self.height):
            row = [0] * self.width
            self.board.append(row)

    def draw(self, win):
        win.blit(self.board_img, (0, 0))

    def update(self, snake_head, snake_body):
        self.board = []
        for i in range(self.height):
            row = [0] * self.width
            self.board.append(row)

        # 2 stands for apple
        self.board[self.apple[0]][self.apple[1]] = 2

        # 1 stands for body/head of the snake
        self.board[snake_head.y // 40][snake_head.x // 40] = 1
        for body in snake_body:
            self.board[body.y // 40][body.x // 40] = 1


