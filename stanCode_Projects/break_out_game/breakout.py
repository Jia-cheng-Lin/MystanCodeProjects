"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman,
and Jerry Liao.

YOUR DESCRIPTION HERE：林嘉誠
"""

from campy.gui.events.timer import pause
from breakoutgraphics import BreakoutGraphics

FRAME_RATE = 1000 / 60  # 120 frames per second
NUM_LIVES = 3  # Number of attempts


def main():
    graphics = BreakoutGraphics()  # call the class

    # know how many lives remained
    live = NUM_LIVES

    # know how many bricks remained
    remain = graphics.brick_row * graphics.brick_col

    # get the default initial velocity for the ball
    dx = graphics.get_dx()  # dx = 0
    dy = graphics.get_dy()  # dy = 0

    # Add animation loop here!
    while True:
        # check it still have lives to play
        if live > 0:
            # check mouse click and can start the game
            if graphics.is_bouncing is True:
                # make sure is first time click or not
                if dx == 0:
                    graphics.set_ball_velocity()
                    dx = graphics.get_dx()
                    dy = graphics.get_dy()
                graphics.ball.move(dx, dy)

                # check need to bounce or not
                # check for left and right
                if graphics.ball.x <= 0 or graphics.ball.x + graphics.ball.width >= graphics.window.width:
                    dx = -dx
                # check for upper
                if graphics.ball.y <= 0:
                    dy = -dy

                # check for lower
                # check for lose life or not
                if graphics.ball.y + graphics.ball.height >= graphics.window.height:
                    # change back for default initial velocity, position and lose one life
                    dx = 0
                    dy = 0
                    live -= 1
                    graphics.set_ball_position()

                    # change back the bollen to let it start again when mouse click
                    graphics.is_bouncing = False

                # check the ball hit object or not
                if graphics.touch() is not None:
                    # print('touch:'+str(graphics.touch()))
                    # check the object is brick, not paddle
                    if graphics.touch() is not graphics.paddle:
                        # remove the brick
                        graphics.window.remove(graphics.touch())
                        # change the direction
                        dy = -dy
                        # clear one brick
                        remain -= 1
                        # check it still have brick or not
                        # no remained brick, then win the game
                        if remain == 0:
                            graphics.win('-15')
                            break
                    else:
                        # the object is paddle
                        # check the ball is move down or up to debug
                        # make sure the ball is move down, and change the direction
                        if dy >= 0:
                            dy = -dy
        # no lives to play, losing the game
        else:
            graphics.lose('-25')
            break

            # print('x:' + str(graphics.ball.x))
            # print('dx:'+str(dx))
            # print('y:' + str(graphics.ball.y))
            # print('dy:' + str(dy))

        pause(FRAME_RATE)  # Have animation spacing


if __name__ == '__main__':
    main()
