"""
File: breakout.py
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

from campy.gui.events.timer import pause
from breakoutgraphics import BreakoutGraphics

FRAME_RATE = 10         # 100 frames per second
NUM_LIVES = 3			# Number of attempts


def main():
    """
    This is a breakout game.
    """
    graphics = BreakoutGraphics()
    lives = NUM_LIVES

    while lives > 0 and graphics.brick_count > 0:
        dx = graphics.get_dx()
        dy = graphics.get_dy()

        graphics.ball.move(dx, dy)
        # 碰撞檢查
        graphics.check_collision()
        # 左右邊界反彈
        if graphics.ball.x < 0 or graphics.ball.x + graphics.ball.width > graphics.window.width:
            graphics._BreakoutGraphics__dx = -dx
        # 上邊界反彈
        if graphics.ball.y < 0:
            graphics._BreakoutGraphics__dy = -dy
        # 下邊界(球掉出去)
        if graphics.ball.y + graphics.ball.height > graphics.window.height:
            lives -= 1
            graphics.reset_ball()
        pause(FRAME_RATE)


if __name__ == '__main__':
    main()
