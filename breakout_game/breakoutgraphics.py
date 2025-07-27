"""
File: breakoutgraphics.py
Name: Yen Ju,Chen
-------------------------
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman, 
and Jerry Liao.

This is a breakout game. The game starts when the player clicks the mouse.
If the ball leaves the window without being caught by the paddle, one life is deducted.
Game end conditions:
Win: All bricks are broken.
Lose: The player runs out of lives.
"""
from campy.graphics.gwindow import GWindow
from campy.graphics.gobjects import GOval, GRect, GLabel
from campy.gui.events.mouse import onmouseclicked, onmousemoved
import random

BRICK_SPACING = 5      # Space between bricks (in pixels). This space is used for horizontal and vertical spacing
BRICK_WIDTH = 40       # Width of a brick (in pixels)
BRICK_HEIGHT = 15      # Height of a brick (in pixels)
BRICK_ROWS = 10        # Number of rows of bricks
BRICK_COLS = 10        # Number of columns of bricks
BRICK_OFFSET = 50      # Vertical offset of the topmost brick from the window top (in pixels)
BALL_RADIUS = 10       # Radius of the ball (in pixels)
PADDLE_WIDTH = 75      # Width of the paddle (in pixels)
PADDLE_HEIGHT = 15     # Height of the paddle (in pixels)
PADDLE_OFFSET = 50     # Vertical offset of the paddle from the window bottom (in pixels)
INITIAL_Y_SPEED = 7    # Initial vertical speed for the ball
MAX_X_SPEED = 5        # Maximum initial horizontal speed for the ball


class BreakoutGraphics:

    def __init__(self, ball_radius=BALL_RADIUS, paddle_width=PADDLE_WIDTH, paddle_height=PADDLE_HEIGHT,
                 paddle_offset=PADDLE_OFFSET, brick_rows=BRICK_ROWS, brick_cols=BRICK_COLS, brick_width=BRICK_WIDTH,
                 brick_height=BRICK_HEIGHT, brick_offset=BRICK_OFFSET, brick_spacing=BRICK_SPACING, title='Breakout'):

        # Create a graphical window, with some extra space
        window_width = brick_cols * (brick_width + brick_spacing) - brick_spacing
        window_height = brick_offset + 3 * (brick_rows * (brick_height + brick_spacing) - brick_spacing)
        self.window = GWindow(width=window_width, height=window_height, title=title)

        # Create a paddle
        self.paddle = GRect(paddle_width, paddle_height)
        self.paddle.color = 'gray'
        self.paddle.fill_color = 'gray'
        self.paddle.filled = True
        self.window.add(self.paddle, x=(window_width - paddle_width) / 2, y=window_height - paddle_offset)

        # Center a filled ball in the graphical window
        self.ball = GOval(ball_radius*2, ball_radius*2)
        self.ball.color = '#D8C3A5'
        self.ball.fill_color = '#D8C3A5'
        self.ball.filled = True
        self.window.add(self.ball, x=(window_width/2) - ball_radius, y=(window_height/2) - ball_radius)

        # Default initial velocity for the ball
        self.__dy = 0
        self.__dx = 0

        # Initialize our mouse listeners
        onmouseclicked(self.start_game)
        onmousemoved(self.move_paddle)

        # Draw bricks
        self.brick_count = 0  # 計算brick數量,數量為0時遊戲結束

        for row in range(brick_rows):
            for col in range(brick_cols):
                x = col * (brick_width + brick_spacing)
                y = brick_offset + row * (brick_height + brick_spacing)
                brick = GRect(brick_width, brick_height, x=x, y=y)
                brick.color = self.give_brick_color(row)
                brick.fill_color = self.give_brick_color(row)
                brick.filled = True
                self.window.add(brick)
                self.brick_count += 1

    def get_dx(self):
        return self.__dx

    def get_dy(self):
        return self.__dy

    def start_game(self, mouse):
        if self.__dy == 0 and self.__dx == 0:
            self.__dx = random.randint(1, MAX_X_SPEED)
            if random.random() > 0.5:
                self.__dx = -self.__dx
            self.__dy = INITIAL_Y_SPEED

    def move_paddle(self, mouse):
        new_x = mouse.x - (self.paddle.width / 2)
        # 限制在視窗內
        if new_x < 0:
            new_x = 0
        if new_x + self.paddle.width > self.window.width:
            new_x = self.window.width - self.paddle.width
        self.paddle.x = new_x

    def check_collision(self):
        for i in [0, self.ball.width]:
            for j in [0, self.ball.height]:
                x = self.ball.x + i
                y = self.ball.y + j
                hit_object = self.window.get_object_at(x, y)

                if hit_object is not None:
                    if hit_object is self.paddle:
                        self.__dy = -self.__dy
                        self.ball.y = self.paddle.y - self.ball.height
                    else:
                        self.window.remove(hit_object)
                        self.__dy = -self.__dy
                        self.brick_count -= 1
                    return  # 碰撞後就不再檢查其他角落

    def reset_ball(self):
        # 移除原本的球
        self.window.remove(self.ball)

        # 建立新的球並加回中央
        self.ball = GOval(self.ball.width, self.ball.height)
        self.ball.color = '#D8C3A5'
        self.ball.fill_color = '#D8C3A5'
        self.ball.filled = True
        self.window.add(self.ball, x=(self.window.width - self.ball.width) / 2,
                        y=(self.window.height - self.ball.height) / 2)

        # 重設為靜止(等user再次點擊)
        self.__dx = 0
        self.__dy = 0

    @staticmethod
    def give_brick_color(row):
        morandi_colors = ['#D8A39D', '#B8C1B1', '#A3B9C9', '#A89F91', '#C1A3B5', '#B9A89F', '#C9CBA3']
        return morandi_colors[row % len(morandi_colors)]
