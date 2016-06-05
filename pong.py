import simplegui
import random

""" PyGame Pong
    An implementation of the classic arcade game, Pong.

    Currently, the keys are set to 'up'/'down' for right paddle,
    and 'w'/'s' for left paddle.
"""

__author__ = ('Dee Reddy', 'deesus@yandex.com')

#############################################


# initialize globals
WIDTH = 600
HEIGHT = 400
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
score1 = score2 = 0
direction = 1
# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left


####################
# helper functions #
####################

def new_game():
    """Starts new game."""

    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel   # these are numbers
    global score1, score2                                       # these are ints

    paddle1_pos =  [[0, HEIGHT/2 - PAD_HEIGHT/2],
                    [PAD_WIDTH, HEIGHT/2 - PAD_HEIGHT/2],
                    [PAD_WIDTH, PAD_HEIGHT/2 + HEIGHT/2],
                    [0, PAD_HEIGHT/2 + HEIGHT/2]]
    paddle2_pos =  [[WIDTH - PAD_WIDTH, HEIGHT/2 - PAD_HEIGHT/2],
                    [WIDTH, HEIGHT/2 - PAD_HEIGHT/2],
                    [WIDTH, PAD_HEIGHT/2 + HEIGHT/2],
                    [WIDTH - PAD_WIDTH, PAD_HEIGHT/2 + HEIGHT/2]]

    paddle1_vel = 0
    paddle2_vel = 0
    spawn_ball()


def spawn_ball():
    """Spawns a new ball (i.e. new round)."""

    global direction, ball_pos, ball_vel    # these are vectors stored as lists
    ball_pos = [WIDTH/2, HEIGHT/3]
    ball_vel = [direction * random.randrange(2, 4), -random.randrange(2, 7)]
    direction *= -1


def bounce():
    """The velocity of ball when it bounces off a paddle."""

    global ball_vel
    ball_vel[0] *= -1
    if abs(ball_vel[0]) < 35:
        ball_vel[0] *= 1.1

################
#   handlers   #
################


def draw(canvas):
    """Paints/draws graphics and text on canvas."""

    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, trace

    # draw median line and lines for gutters:
    canvas.draw_line((WIDTH / 2, 0), (WIDTH / 2, HEIGHT), 1, "White")
    canvas.draw_line((PAD_WIDTH, 0), (PAD_WIDTH, HEIGHT), 1, "White")
    canvas.draw_line((WIDTH - PAD_WIDTH, 0), (WIDTH - PAD_WIDTH, HEIGHT), 1, "White")
    canvas.draw_line((0, HEIGHT/2), (WIDTH, HEIGHT/2), 1, "White")

    # update ball:
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

    # draw ball:
    canvas.draw_circle(ball_pos, BALL_RADIUS, 1, 'white', 'white')

    # update paddle's vertical position, keep paddle on the screen:
    # left paddle:
    if (paddle1_pos[0][1] + paddle1_vel >= 0) and \
    (paddle1_pos[3][1] + paddle1_vel <= HEIGHT):
        for coordinate in paddle1_pos:
            coordinate[1] += paddle1_vel

    # right paddle:
    if (paddle2_pos[0][1] + paddle2_vel >= 0) and \
    (paddle2_pos[3][1] + paddle2_vel <= HEIGHT):
        for coordinate in paddle2_pos:
            coordinate[1] += paddle2_vel

    # draw paddles:
    # (n.b. polygon lines are drawn in clockwise direction)
    canvas.draw_polygon(paddle1_pos, 1, "red", "red")
    canvas.draw_polygon(paddle2_pos, 1, "blue", "blue")

    # determine whether paddle and ball collide:
    # vertical bounce:
    if ball_pos[1] + (BALL_RADIUS + 1) >= HEIGHT - 1:
        ball_vel[1] *= -1
    elif ball_pos[1] - (BALL_RADIUS + 1) <= 0:
        ball_vel[1] *= -1
    # horizontal bounce:
    # right side:
    if ball_pos[0] + (BALL_RADIUS + 1) >= WIDTH - PAD_WIDTH - 1:
        if paddle2_pos[0][1] - (BALL_RADIUS+1) <= \
        ball_pos[1] <= paddle2_pos[3][1] + (BALL_RADIUS+1):
            bounce()
        else:
            if score1 < 98:
                score1 += 1
            spawn_ball()
    # left side:
    if ball_pos[0] - (BALL_RADIUS + 1) <= PAD_WIDTH:
        if paddle1_pos[0][1] - (BALL_RADIUS + 1) <= ball_pos[1] <= \
        paddle1_pos[3][1] + (BALL_RADIUS+1):
            bounce()
        else:
            if score2 < 98:
                score2 += 1
            spawn_ball()

    # draw scores:
    padding = 14        # the space of a single digit

    if score2 >= 10:
        padding = 1
    canvas.draw_text(str(score1), (WIDTH/2 - 26, 20), 20, 'White', 'monospace')
    canvas.draw_text(str(score2), (WIDTH/2 + padding, 20), 20, 'White', 'monospace')


def keydown(key):
    """Handles user keyboard-down input.

        Args:
            key: user keyboard mapping
    """

    global paddle1_vel, paddle2_vel

    # left player:
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel -= 3
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel += 3
    # right player:
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel -= 3
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel += 3


def keyup(key):
    """Handles user keyboard-up input.

        Args:
            key: user keyboard mapping
    """

    global paddle1_vel, paddle2_vel

    if key == simplegui.KEY_MAP["w"] or key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 0
    if key == simplegui.KEY_MAP["up"] or key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 0


def button_handler():
    """Handles 'new game' button."""

    global score1, score2
    score1 = score2 = 0
    new_game()

################
# create frame #
################

frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("new game", button_handler,  100)

###############
# start frame #
###############

new_game()
frame.start()
