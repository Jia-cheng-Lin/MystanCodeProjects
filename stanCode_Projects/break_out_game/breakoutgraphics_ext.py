"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman, 
and Jerry Liao

YOUR DESCRIPTION HERE：林嘉誠
"""
from campy.graphics.gwindow import GWindow
from campy.graphics.gobjects import GOval, GRect, GLabel
from campy.gui.events.mouse import onmouseclicked, onmousemoved
import random

BRICK_SPACING = 5      # Space between bricks (in pixels). This space is used for horizontal and vertical spacing.
BRICK_WIDTH = 40       # Height of a brick (in pixels).
BRICK_HEIGHT = 15      # Height of a brick (in pixels).
BRICK_ROWS = 10        # Number of rows of bricks.
BRICK_COLS = 10        # Number of columns of bricks.
BRICK_OFFSET = 50      # Vertical offset of the topmost brick from the window top (in pixels).
BALL_RADIUS = 10       # Radius of the ball (in pixels).
PADDLE_WIDTH = 75      # Width of the paddle (in pixels).
PADDLE_HEIGHT = 15     # Height of the paddle (in pixels).
PADDLE_OFFSET = 50     # Vertical offset of the paddle from the window bottom (in pixels).

INITIAL_Y_SPEED = 7    # Initial vertical speed for the ball.
MAX_X_SPEED = 5        # Maximum initial horizontal speed for the ball.

# Global Variable
ball = GOval(BALL_RADIUS, BALL_RADIUS)  # ball
ball_is_moving = False                  # check the game state
end = GLabel('Congratulation!!')        # add the label when you win
over = GLabel('Game over!')             # add the label when you lose
score = 0
score_label = GLabel('Score:' + str(score))


class BreakoutGraphics:
    # constructor
    def __init__(self, ball_radius=BALL_RADIUS, paddle_width=PADDLE_WIDTH,
                 paddle_height=PADDLE_HEIGHT, paddle_offset=PADDLE_OFFSET,
                 brick_rows=BRICK_ROWS, brick_cols=BRICK_COLS,
                 brick_width=BRICK_WIDTH, brick_height=BRICK_HEIGHT,
                 brick_offset=BRICK_OFFSET, brick_spacing=BRICK_SPACING,
                 title='Breakout', add=10,):

        # Create a graphical window, with some extra space
        window_width = brick_cols * (brick_width + brick_spacing) - brick_spacing
        window_height = brick_offset + 3 * (brick_rows * (brick_height + brick_spacing) - brick_spacing)
        self.window = GWindow(width=window_width, height=window_height, title=title)

        # Create a paddle
        self.paddle = GRect(width=paddle_width, height=paddle_height)
        self.paddle_offset = paddle_offset
        self.paddle.filled = True
        self.window.add(self.paddle,
                        (self.window.width - self.paddle.width) / 2,
                        (self.window.height-self.paddle_offset))

        # Center a filled ball in the graphical window
        self.ball = GOval(2*ball_radius, 2*ball_radius)
        self.ball.filled = True

        # ball position at the beginning
        start_x = (self.window.width - self.ball.width) / 2
        start_y = (self.window.height - self.ball.height) / 2
        self.window.add(self.ball, start_x, start_y)

        # Default initial velocity for the ball
        self.__dx = 0  # horizontal speed
        self.__dy = 0  # vertical speed
        self.is_bouncing = False

        # Initialize our mouse listeners
        onmouseclicked(self.real_start)
        onmousemoved(self.move)

        # Draw bricks
        self.brick_offset = brick_offset
        self.brick_row = brick_rows
        self.brick_col = brick_cols
        self.brick_spacing = brick_spacing

        # Put bricks and draw color
        for i in range(self.brick_row):
            for j in range(self.brick_col):
                self.brick = GRect(width=brick_width, height=brick_height)
                self.brick.filled = True
                if i <= 1:
                    self.brick.fill_color = 'red'
                elif i <= 3:
                    self.brick.fill_color = 'orange'
                elif i <= 5:
                    self.brick.fill_color = 'yellow'
                elif i <= 7:
                    self.brick.fill_color = 'green'
                elif i <= 9:
                    self.brick.fill_color = 'blue'
                self.window.add(self.brick,
                                (self.brick.width+self.brick_spacing)*j,
                                (self.brick.height+self.brick_spacing)*i+self.brick_offset)
        # extend
        self.add = add

    # let you use one life to play game
    def real_start(self, event):
        if self.is_bouncing is False:
            self.is_bouncing = True
            # self.set_ball_velocity()
            # print('correct')
            # print('click:'+str(self.is_bouncing))

    # let paddle move with mouse move
    def move(self, event):
        move_paddle = self.paddle

        # make sure paddle will not move out of window
        if self.paddle.width/2 <= event.x <= self.window.width-self.paddle.width/2:

            # paddle.y is fixed, center of paddle move by mouse
            move_paddle.x = event.x - self.paddle.width/2
            move_paddle.y = self.window.height-self.paddle_offset

    # Give the ball position at the beginning
    def set_ball_position(self):
        self.ball.x = (self.window.width - self.ball.width) / 2
        self.ball.y = (self.window.height - self.ball.height) / 2

    # get different combination of speed
    def set_ball_velocity(self):
        self.__dy = INITIAL_Y_SPEED
        self.__dx = random.randint(1, MAX_X_SPEED)
        if random.random() > 0.5:
            self.__dx = -self.__dx
        print('dx is :'+str(self.__dx))
        print('dy is :' + str(self.__dy))

    # dx is private, so need use getter to get
    def get_dx(self):
        # Getter
        return self.__dx

    # dy is private, so need use getter to get
    def get_dy(self):
        # Getter
        return self.__dy

    # check ball touch the object or not
    def touch(self):
        # coordinates of the four corners of ball
        up_left = self.window.get_object_at(self.ball.x, self.ball.y)
        up_right = self.window.get_object_at(self.ball.x+self.ball.width, self.ball.y)
        down_left = self.window.get_object_at(self.ball.x, self.ball.y+self.ball.height)
        down_right = self.window.get_object_at(self.ball.x+self.ball.width, self.ball.y+self.ball.height)
        # check ball touch or not, and return the object that ball touch
        if up_left is not None:
            return up_left
        if up_right is not None:
            return up_right
        if down_left is not None:
            return down_left
        if down_right is not None:
            return down_right
        return None

    # add label when you win the game
    def win(self, font='Dialog-20-italic'):
        end.color = 'red'
        end.font = font
        # add label at center
        self.window.add(end, (self.window.width-end.width)/2, (self.window.height-end.height)/2)

    # add label when you lose the game
    def lose(self, font='Dialog-20-italic'):
        over.color = 'red'
        over.font = font
        # add label at center
        self.window.add(over, (self.window.width-over.width)/2, (self.window.height-over.height)/2)
