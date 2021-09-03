"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman,
and Jerry Liao.

YOUR DESCRIPTION HERE：林嘉誠
"""

from campy.gui.events.timer import pause
from campy.graphics.gobjects import GOval, GRect, GLabel
from breakoutgraphics_ext import BreakoutGraphics

FRAME_RATE = 1000 / 60  # 120 frames per second
NUM_LIVES = 3           # Number of attempts
ACCELERATE = 1.05       # accelerate after clear one brick
ADD = 10                # score added when brick clear

# Global Variable
score = 0
score_label = GLabel('Score:' + str(score))


def main():
    global score
    graphics = BreakoutGraphics()  # call the class

    # Game score
    score_label.font = 'Dialog-20-italic'
    graphics.window.add(score_label, 0, graphics.window.height)

    # know how many lives remained
    live = NUM_LIVES
    remain_life = GLabel('Lives:' + str(live))
    remain_life.font = 'Dialog-20-italic'
    graphics.window.add(remain_life, graphics.window.width-remain_life.width, graphics.window.height)

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
                    remain_life.text = 'Lives' + str(live)
                    graphics.set_ball_position()

                    # change back the bollen to let it start again when mouse click
                    graphics.is_bouncing = False

                # check the ball hit object or not
                if graphics.touch() is not None:
                    # print('touch:'+str(graphics.touch()))
                    # check the object is brick, not paddle, score, life
                    if graphics.touch() is not graphics.paddle and graphics.touch() is not remain_life and graphics.touch() is not score_label:
                        # remove the brick
                        graphics.window.remove(graphics.touch())
                        # change the direction
                        dy = -dy * ACCELERATE
                        dx = dx * ACCELERATE
                        # clear one brick
                        remain -= 1
                        score += ADD
                        score_label.text = 'Score' + str(score)

                        # check it still have brick or not
                        # no remained brick, then win the game
                        if remain == 0:
                            graphics.win('-15')
                            break
                    else:
                        # make sure the object is paddle
                        # check the ball is move down or up to debug
                        # make sure the ball is move down, and change the direction
                        if graphics.touch() is not remain_life and graphics.touch() is not score_label:
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
