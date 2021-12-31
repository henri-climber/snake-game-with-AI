class SnakeHead:
    def __init__(self, x, y, facing, img_up, img_left, img_down, img_right):
        self.x = x
        self.y = y
        self.facing = facing
        self.img_up = img_up
        self.img_left = img_left
        self.img_down = img_down
        self.img_right = img_right

        self.is_alive = True
        self.vel = 40

    def draw(self, win, snakes):
        if self.facing == "down":
            win.blit(self.img_down, (self.x, self.y))
        elif self.facing == "right":
            win.blit(self.img_right, (self.x, self.y))
        elif self.facing == "up":
            win.blit(self.img_up, (self.x, self.y))
        elif self.facing == "left":
            win.blit(self.img_left, (self.x, self.y))

        for snake in snakes:
            snake.draw(win)

    def move(self, snakes):
        for i in range(len(snakes) - 1, 0, -1):
            snake_in_front = snakes[i - 1]
            snakes[i].x = snake_in_front.x
            snakes[i].y = snake_in_front.y
            snakes[i].facing = snake_in_front.facing

        snakes[0].x = self.x
        snakes[0].y = self.y
        snakes[0].facing = self.facing

        if self.facing == "down":
            self.y += self.vel
        elif self.facing == "right":
            self.x += self.vel
        elif self.facing == "up":
            self.y -= self.vel
        elif self.facing == "left":
            self.x -= self.vel

    def collide(self, width, height, snakes):
        # out of border
        if self.x > width or self.x < 0:
            return True
        if self.y > height or self.y < 0:
            return True

        # if head crashes in body
        for snake in snakes:
            if self.x == snake.x and self.y == snake.y:
                return True
        return False


class SnakeBody:
    def __init__(self, x, y, facing, img_horizontal, img_vertical, img_body):
        self.x = x
        self.y = y
        self.facing = facing
        self.img_horizontal = img_horizontal
        self.img_vertical = img_vertical
        self.img_body = img_body

    def draw(self, win):
        win.blit(self.img_body, (self.x, self.y))

