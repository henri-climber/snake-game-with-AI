class Apple:
    def __init__(self, x, y, apple_img):
        self.x = x
        self.y = y
        self.apple_img = apple_img

    def draw(self, win):
        win.blit(self.apple_img, (self.x, self.y))

