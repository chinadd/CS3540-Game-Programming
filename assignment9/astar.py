import random, sys
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import heapq

# constants
CELL_SIZE = 10
SIZE = 40

# view state
cells = None # grid of cells of the world
start = None # starting position
searched = set() # set of cells searched for path
path = None # list of cells along path from start to goal


def route(are, was):
    route = [are]
    while are in was:
        are = was[are]
        if are is None:
            break
        route.append(are)
    route.reverse()
    return route


def dist(x, y):
    return ((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2) ** 0.5


# run astar
def astar(goal):
    global cells, start

    # TODO: implement astar, return a list of the cells from the start to goal (or None if there is no path)
    #  and a set of the cells searched

    interior = []
    already = set()
    started_at = dict()
    area = dict()

    already.add(start)
    started_at[start] = None
    area[start] = 0.0

    heapq.heappush(interior, (dist(start, goal), start))
    while len(interior) != 0:
        at = heapq.heappop(interior)[1]

        if at == goal:
            return route(at, started_at), already

        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
            x = at[0] + dx
            y = at[1] + dy

            if x < 0 or x >= SIZE or y < 0 or y >= SIZE:
                continue

            if cells[x][y]:
                continue

            next_point = (x, y)
            total_area = area[at] + dist(at, next_point)
            
            if next_point not in area or total_area < area[next_point]:
                area[next_point] = total_area
                priority = total_area + dist(next_point, goal)
                heapq.heappush(interior, (priority, next_point))
                already.add(next_point)
                started_at[next_point] = at

    return None, set()


# create a new world
def newWorld():
    global cells, start, searched, path

    cells = [[0 for i in xrange(SIZE)] for i in xrange(SIZE)]
    for ii in xrange(30):
        ll = random.randint(3, 10)
        xx = random.randint(0, SIZE - 1 - ll)
        yy = random.randint(0, SIZE - 1 - ll)
        if random.randint(0, 1) == 0:
            dx = 1
            dy = 0
        else:
            dx = 0
            dy = 1

        for jj in xrange(ll):
            if xx >= SIZE or yy >= SIZE:
                break

            cells[xx][yy] = 1
            xx += dx
            yy += dy

    while True:
        start = (random.randint(0, SIZE - 1), random.randint(0, SIZE - 1))
        if cells[start[0]][start[1]] == 0:
            break

    searched = set()
    path = None


# mouse button handler
def mouseButton(button, state, xx, yy):
    global cells, start, searched, path

    if button != GLUT_LEFT_BUTTON:
        return

    if state != GLUT_DOWN:
        return

    pt = (xx / CELL_SIZE, (SIZE * CELL_SIZE - yy - 1) / CELL_SIZE)

    path, searched = astar(pt)

    glutPostRedisplay()


# function for handling key down
def keyboard(c, x, y):
    if c == ' ':
        newWorld()

        glutPostRedisplay()


# function for displaying a cell
def displayCell(xx, yy):
    glVertex2f((xx + 0) * CELL_SIZE, (yy + 0) * CELL_SIZE)
    glVertex2f((xx + 1) * CELL_SIZE, (yy + 0) * CELL_SIZE)
    glVertex2f((xx + 1) * CELL_SIZE, (yy + 1) * CELL_SIZE)
    glVertex2f((xx + 0) * CELL_SIZE, (yy + 1) * CELL_SIZE)


# function for displaying the game screen
def display():
    global cells, start, searched, path

    glClear(GL_COLOR_BUFFER_BIT)

    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    gluOrtho2D(0, CELL_SIZE * SIZE, 0, CELL_SIZE * SIZE);
 
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();

    glBegin(GL_QUADS)
    for xx in xrange(SIZE):
        for yy in xrange(SIZE):
            if (xx, yy) == start:
                glColor3f(0.8, 0.0, 0.8)
            elif path != None and (xx, yy) in path:
                if cells[xx][yy] == 1:
                    glColor3f(1.0, 0.0, 0.0)
                else:
                    idx = path.index((xx, yy))
                    glColor3f(0.0, 0.2 + 0.8 * (idx / float(len(path) - 1)), 0.0)
            elif searched != None and (xx, yy) in searched:
                if cells[xx][yy] == 1:
                    glColor3f(1.0, 0.0, 0.0)
                else:
                    glColor3f(0.0, 0.1, 0.3)
            elif cells[xx][yy] == 1:
                glColor3f(0.5, 0.5, 0.5)
            else:
                glColor3f(0.0, 0.0, 0.0)

            displayCell(xx, yy)
    glEnd()

    glutSwapBuffers()


# startup
random.seed(12345)
newWorld()

glutInit(sys.argv)
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
glutInitWindowSize(CELL_SIZE * SIZE, CELL_SIZE * SIZE)
glutCreateWindow('CS3540')
glutDisplayFunc(display)
glutKeyboardFunc(keyboard)
glutMouseFunc(mouseButton)
glutMainLoop()
