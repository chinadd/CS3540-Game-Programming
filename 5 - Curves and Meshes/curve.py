import random, sys
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# constants
SIZE = 480
HANDLE_SIZE = 9
FLATNESS_EPSILON = 0.00005

TYPE_BEZIER = 0
TYPE_CATMULLROM = 1

# view state
ctype = TYPE_BEZIER
handles = []
activeHandle = None
showHandles = True


def drawBezier(a0, b0, c0, d0):
    d1 = ((a0[0] - b0[0]) ** 2 + (a0[1] - b0[1]) ** 2) ** 0.5
    d2 = ((b0[0] - c0[0]) ** 2 + (b0[1] - c0[1]) ** 2) ** 0.5
    d3 = ((c0[0] - d0[0]) ** 2 + (c0[1] - d0[1]) ** 2) ** 0.5
    d4 = ((a0[0] - d0[0]) ** 2 + (a0[1] - d0[1]) ** 2) ** 0.5

    if ((d1 + d2 + d3) / (d4 + FLATNESS_EPSILON ** 2)) < (FLATNESS_EPSILON + 1):
        glVertex2f(a0[0], a0[1])
        glVertex2f(d0[0], d0[1])
    else:
        a1 = 0.5 * (a0[0] + b0[0]), 0.5 * (a0[1] + b0[1])
        b1 = 0.5 * (b0[0] + c0[0]), 0.5 * (b0[1] + c0[1])
        c1 = 0.5 * (c0[0] + d0[0]), 0.5 * (c0[1] + d0[1])
        a2 = 0.5 * (a1[0] + b1[0]), 0.5 * (a1[1] + b1[1])
        b2 = 0.5 * (b1[0] + c1[0]), 0.5 * (b1[1] + c1[1])
        a3 = 0.5 * (a2[0] + b2[0]), 0.5 * (a2[1] + b2[1])
        drawBezier(a0, a1, a2, a3)
        drawBezier(a3, b2, c1, d0)

# function for drawing a curve
def drawCurve():
    global ctype, handles

    if ctype == TYPE_BEZIER:
        # TODO: draw Bezier curve from handles
        for a in xrange(0, len(handles) - 3, 3):
            drawBezier(handles[a], handles[a+1], handles[a+2], handles[a+3])
        pass

    else:
        # TODO: draw Catmull-Rom curve from handles
        for a in xrange(0, len(handles) - 3):
            a0 = handles[a]
            b0 = handles[a + 1]
            c0 = handles[a + 2]
            d0 = handles[a + 3]
            verts = []
            for i in xrange(11):
                t = i / 10
                a1 = (b0[0] + t *
                        (-0.5 * a0[0] + 0.5 * c0[0]) +
                        (t ** 2) *
                        (1 * a0[0] - 2.5 * b0[0] + 2 * c0[0] - 0.5 * d0[0]) +
                        (t ** 3) *
                        (-0.5 * a0[0] + 1.5 * b0[0] - 1.5 * c0[0] + 0.5 * d0[0])
                     )
                b1 = (b0[1] + t *
                        (-0.5 * a0[1] + 0.5 * c0[1]) +
                        (t ** 2) *
                        (1 * a0[1] - 2.5 * b0[1] + 2 * c0[1] - 0.5 * d0[1]) +
                        (t ** 3) *
                        (-0.5 * a0[1] + 1.5 * b0[1] - 1.5 * c0[1] + 0.5 * d0[1])
                     )
                verts.append((a1, b1))

            for a2, b2 in zip(verts, verts[1:]):
                glVertex2f(a2[0], a2[1])
                glVertex2f(b2[0], b2[1])
        pass


# mouse button handler
def mouseButton(button, state, mx, my):
    global handles, activeHandle

    if button != GLUT_LEFT_BUTTON:
        return

    if state == GLUT_DOWN:
        closest = 1e100
        for ii, (hx, hy) in enumerate(handles):
            if abs(hx - mx) <= HANDLE_SIZE / 2 and abs(hy - my) <= HANDLE_SIZE / 2:
                distsq = (hx - mx) ** 2 + (hy - my) ** 2
                if distsq < closest:
                    closest = distsq
                    activeHandle = ii

        if activeHandle == None:
            handles.append((mx, my))
            activeHandle = len(handles) - 1

    if state == GLUT_UP:
        activeHandle = None

    glutPostRedisplay()


# mouse motion handler
def mouseMotion(mx, my):
    global handles, activeHandle

    if activeHandle != None:
        handles[activeHandle] = (mx, my)

        glutPostRedisplay()


# function for handling key down
def keyboard(ch, mx, my):
    global ctype, handles, activeHandle, showHandles

    if ch == ' ':
        handles = []
        activeHandle = None

    elif ch.lower() == 't':
        if ctype == TYPE_BEZIER:
            ctype = TYPE_CATMULLROM
        else:
            ctype = TYPE_BEZIER

    elif ch.lower() == 's':
        showHandles = not showHandles

    glutPostRedisplay()


# function for displaying the game screen
def display():
    global handles, activeHandle, showHandles

    glClear(GL_COLOR_BUFFER_BIT)

    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    gluOrtho2D(0, SIZE, SIZE, 0);
 
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();

    if showHandles:
        glColor3f(0.2, 0.2, 0.2)
        glBegin(GL_LINE_STRIP)
        for hx, hy in handles:
            glVertex2f(hx, hy)
        glEnd()

    glColor3f(0.5, 0.5, 0.5)
    glBegin(GL_LINES)
    drawCurve()
    glEnd()

    if showHandles:
        glBegin(GL_QUADS)
        for ii, (hx, hy) in enumerate(handles):
            if activeHandle != None and activeHandle == ii:
                glColor3f(0.5, 0.5, 1.0)
            else:
                glColor3f(0.8, 0.8, 0.8)

            glVertex2f(hx - 0.5 * HANDLE_SIZE, hy - 0.5 * HANDLE_SIZE)
            glVertex2f(hx + 0.5 * HANDLE_SIZE, hy - 0.5 * HANDLE_SIZE)
            glVertex2f(hx + 0.5 * HANDLE_SIZE, hy + 0.5 * HANDLE_SIZE)
            glVertex2f(hx - 0.5 * HANDLE_SIZE, hy + 0.5 * HANDLE_SIZE)
        glEnd()

    glutSwapBuffers()


# startup
glutInit(sys.argv)
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
glutInitWindowSize(SIZE, SIZE)
glutCreateWindow('CS3540')
glutDisplayFunc(display)
glutKeyboardFunc(keyboard)
glutMouseFunc(mouseButton)
glutMotionFunc(mouseMotion)
glutPassiveMotionFunc(mouseMotion)
glutMainLoop()
