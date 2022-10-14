# snake.py #
# Snake In Terminal by nozze #
import os, time, keyboard, random

class Board:
    WIDTH = 15
    HEIGHT = 15

    def get_pixel(self, color: tuple[int, int, int]):
        return f"\u001b[48;2;{color[0]};{color[1]};{color[2]}m  \u001b[0m"

    def get_width(self):
        return self.WIDTH
    
    def get_height(self):
        return self.HEIGHT

    def clear(self):
        os.system("cls")
    
    def draw(self, points, player_mass):
        self.clear()
        x, y = 1, 1
        game = ""
        for _ in range(self.HEIGHT):
            for _ in range(self.WIDTH):
                occupied = False
                for point in points:
                    if not occupied:
                        if point.position == (x, y):
                            occupied = True
                            game += self.get_pixel(point.color)
                if not occupied:
                    game += self.get_pixel((38, 24, 71))
                x += 1
            game += "\n"
            x = 1
            y += 1
        game += f"\u001b[1;38;2;0;255;0mMASS: {player_mass}\u001b[0m\n"
        game += f"\u001b[1;38;2;255;0;0mE TO QUIT\u001b[0m\n"
        print(game)

class Point:
    def __init__(self, color: tuple[int, int, int], position: tuple[int, int]):
        self.color = color
        self.position = position

class Snake:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dir = "down"
        set_key = lambda key, dir: keyboard.add_hotkey(key, lambda: snake.change_direction(dir))
        set_key("w", "up")
        set_key("s", "down")
        set_key("d", "right")
        set_key("a", "left")
        keyboard.add_hotkey("e", lambda: snake.quit())
        self.mass = 1
        self.history = [(x, y)]
        self.apple = (7, 7)
        self.quit_game = False
    
    def change_direction(self, direction):
        if direction == "up":
            if self.dir != "down":
                self.dir = direction
        elif direction == "down":
            if self.dir != "up":
                self.dir = direction
        elif direction == "left":
            if self.dir != "right":
                self.dir = direction
        elif direction == "right":
            if self.dir != "left":
                self.dir = direction

    def eat_apple(self, board):
        is_free = True
        while is_free:
            self.apple = (
                random.randint(1, board.get_width()),
                random.randint(1, board.get_height())
            )
            for point in self.history:
                if self.apple != point:
                    is_free = False
        self.mass += 1

    def die(self):
        self.apple = (8, 7)
        self.x = 5
        self.y = 5
        self.history = [(int(self.x), int(self.y))]
        self.mass = 1

    def quit(self):
        self.quit_game = True

    def update(self, board):
        if self.dir == "up":
            self.y -= 1
            if self.y < 1:
                self.y = board.get_height()
        elif self.dir == "down":
            self.y += 1
            if self.y > board.get_height():
                self.y = 1
        elif self.dir == "left":
            self.x -= 1
            if self.x < 1:
                self.x = board.get_width()
        elif self.dir == "right":
            self.x += 1
            if self.x > board.get_width():
                self.x = 1

        if (self.x, self.y) == self.apple:
            self.eat_apple(board)
        
        self.history.append((int(self.x), int(self.y)))
        if len(self.history) > self.mass:
            self.history.pop(0)

        if len(set(self.history)) < len(self.history):
            self.die()
    
    def get_points(self):
        points = []
        for i, point in enumerate(self.history):
            color = ()
            if (i % 2) == 0 or i == 0:
                color = (0, 255, 0)
            else:
                color = (0, 155, 0)
            points.append(Point(color, point))
        points.append(Point((255, 0, 0), self.apple))
        return points

snake = Snake(5, 5)
board = Board()
while not snake.quit_game:
    snake.update(board)
    board.draw(snake.get_points(), snake.mass)
    time.sleep(0.1)