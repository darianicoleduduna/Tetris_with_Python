from shape import Shape
import time

class Tetris:
    def __init__(self, h, w):
        self.height = h
        self.width = w
        self.grid = [[0] * w for _ in range(h)]
        self.score = 0
        self.state = "start"
        self.new_shape()
        self.x = 100
        self.y = 60
        self.zoom = 30
        self.shape = None
        self.drop_time = 0  # the time it takes to process that 2 figures intersected 
        self.drop_delay = 0.5  # 2-seconds delay
        self.high_score=0

    def new_shape(self):
        self.shape = Shape(3, 0)

    def intersects(self):
        intersection = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.shape.image():
                    if i + self.shape.y > self.height - 1 or j + self.shape.x > self.width - 1 or j + self.shape.x < 0 or self.grid[i + self.shape.y][j + self.shape.x] > 0:
                        intersection = True
        return intersection

    def completed_line(self):
        lines = 0
        for i in range(1, self.height):
            zeros = 0
            for j in range(self.width):
                if self.grid[i][j] == 0:
                    zeros += 1
            if zeros == 0:
                lines += 1
                for k in range(i, 1, -1):
                    for j in range(self.width):
                        self.grid[k][j] = self.grid[k - 1][j]
        self.score += lines ** 2

    def stop_fig(self):
        # When the piece has just landed, the timer starts
        if self.drop_time == 0:
            self.drop_time = time.time()

        # Check if the 2-second delay has passed
        if time.time() - self.drop_time >= self.drop_delay:
            for i in range(4):
                for j in range(4):
                    if i * 4 + j in self.shape.image():
                        self.grid[i + self.shape.y][j + self.shape.x] = self.shape.color
            self.completed_line()
            self.new_shape()
            self.drop_time = 0  # Reset the timer
            if self.intersects():
                self.state = "game_over"

    def go_fast(self):
        while not self.intersects():
            self.shape.y += 1
        self.shape.y -= 1
        self.stop_fig()

    def go_down(self):
        self.shape.y += 1
        if self.intersects():
            self.shape.y -= 1
            self.stop_fig()

    def go_side(self, dx):
        old_x = self.shape.x
        self.shape.x += dx
        if self.intersects():
            self.shape.x = old_x

    def rotate(self):
        old_rotation = self.shape.rotation
        self.shape.rotate()
        if self.intersects():
            self.shape.rotation = old_rotation

    def play_again(self):
        self.score = 0
        self.state = "start"
        self.grid = [[0] * self.width for _ in range(self.height)] # clearing the previous grid 
        self.new_shape()
        self.drop_time = 0


