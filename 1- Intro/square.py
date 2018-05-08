import sys
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# constants
TIMER_TIME = 33
SQUARE_SPEED = 0.2
SQUARE_SIZE = 0.1

# keep track of which keys are down
keys_down = set()

# game state
square_x = 0.5
square_y = 0.5


# function to draw a rectangle
def drawrect(cx, cy, w2, h2):
    glBegin(GL_QUADS)
    glVertex2f(cx - w2, cy - h2)
    glVertex2f(cx + w2, cy - h2)
    glVertex2f(cx + w2, cy + h2)
    glVertex2f(cx - w2, cy + h2)
    glEnd()


# function for handling key down
def keyboard(c, x, y):
    global keys_down

    keys_down.add(c.lower())

# function for handling key up
def keyboardup(c, x, y):
    global keys_down

    keys_down.discard(c.lower())

# handle state update on timer
def timer(value):
    global keys_down
    global square_x, square_y

    dt = TIMER_TIME / 1000.0

    # TODO: update state
    if ('a' in keys_down):
	square_x -= dt * SQUARE_SPEED
    if ('s' in keys_down):
	square_y -= dt * SQUARE_SPEED
    if ('d' in keys_down):
	square_x += dt * SQUARE_SPEED
    if ('w' in keys_down):
	square_y += dt * SQUARE_SPEED

    glutPostRedisplay()
    glutTimerFunc(TIMER_TIME, timer, 0)


# function for displaying the game screen
def display():
    global keys_down
    global square_x, square_y

    glClear(GL_COLOR_BUFFER_BIT)

    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    gluOrtho2D(0.0, 1.0, 0.0, 1.0);
 
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();

    glColor3f(1, 1, 1)

    # TODO: display square
    drawrect(square_x, square_y, SQUARE_SIZE, SQUARE_SIZE)

    glutSwapBuffers()


# startup
glutInit(sys.argv)
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
glutInitWindowSize(640, 640)
glutCreateWindow('CS3540')
glutDisplayFunc(display)
glutKeyboardFunc(keyboard)
glutKeyboardUpFunc(keyboardup)
glutTimerFunc(TIMER_TIME, timer, 0)
glutMainLoop()
