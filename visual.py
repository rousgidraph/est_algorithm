import sys
import  pygame
from  pygame.locals import *
import solution
import math


#constants
filename = "001.env"
_bounds = []#X_low,X_high,y_low,y_high
#SCREENSIZE = WIDTH,HEIGHT = 600,600
SCREENSIZE = WIDTH,HEIGHT = 800,800

BLACK = (0,0,0)
WHITE = (255,255,255)
GREY = (160,160,160)
PADDING = PADTOPBOTTOM, PADLEFTRIGHT = 60, 60
divs = 100
_obstacles = []
#y_scale = 0
#x_scale = 0

#VARS 
_VARS = {'surf': False }

def main():
    solution.read_env_file(filename,_obstacles,_bounds)
    calc_scale()
    #print("this is yscale ",y_scale)
    #print(-1*y_scale)
    #print(_obstacles[0].__str__())
    global n1 
    n1 = solution.Node(5,9,"01")
    global n2
    n2 = solution.Node(0,0,"origi")
    draw_line(n1,n2)

    pygame.init() # initialize the engine 
    _VARS['surf'] = pygame.display.set_mode(SCREENSIZE)
    
    while True:
        checkEvents()
        _VARS['surf'].fill(GREY)
        drawGrid(divs)
        #draw_obstacles()
        #draw_point(2,2)
        pygame.display.flip()
        pygame.display.update()
        

def calc_scale():
    #print(_bounds)
    _height = SCREENSIZE[1]-(2*PADDING[0])
    _width = SCREENSIZE[0]-(2*PADDING[1])
    max_x = abs(_bounds[0]) +   abs(_bounds[1])
    max_y = abs(_bounds[2]) +   abs(_bounds[3])
    global x_scale 
    x_scale= _width / max_x
    global y_scale 
    y_scale= _height / max_y
    #this is a bad idea incase of issues start here 
    y_scale = x_scale = 10
    #print("this is yscale ",y_scale)
    pass

def coord(x,y):
    y = float(y) * abs(y_scale) 
    y_origin = SCREENSIZE[1] / 2
    _y = y_origin + y
       
       
    x = float(x) * abs(x_scale) 
    x_origin = SCREENSIZE[0] / 2
    _x = x_origin + x
       
    
    #print(y_scale,_x,_y)
    return (_x,_y)

def draw_circ(_x,_y,_radius):
    pygame.draw.circle(_VARS['surf'],WHITE,coord(_x,_y),float(_radius)*5)
    pass


def draw_point(_x,_y):
    pygame.draw.circle(_VARS['surf'],BLACK,coord(_x,_y),2)
    pass

def draw_line(n1,n2):
    x_1 = float(n1.get_x())
    y_1 = float(n1.get_y())
    x_2 = float(n2.get_x())
    y_2 = float(n2.get_y())
    print(x_1)
    #pygame.draw.line(_VARS['surf'],coord(x_1,y_1),coord(x_2,y_2))
    pass

def draw_node(node):
    pass

def draw_obstacles():
    for obst in _obstacles:
        draw_circ(obst.get_x(),obst.get_y(),obst.get_rad())
    pass


def drawGrid(divisions):
    # DRAW Rectangle
    # TOP lEFT TO RIGHT
    pygame.draw.line(
      _VARS['surf'], BLACK,
      (0 + PADLEFTRIGHT, 0 + PADTOPBOTTOM),
      (WIDTH - PADLEFTRIGHT, 0 + PADTOPBOTTOM), 2)
    # BOTTOM lEFT TO RIGHT
    pygame.draw.line(
      _VARS['surf'], BLACK,
      (0 + PADLEFTRIGHT, HEIGHT - PADTOPBOTTOM),
      (WIDTH - PADLEFTRIGHT, HEIGHT - PADTOPBOTTOM), 2)
    # LEFT TOP TO BOTTOM
    pygame.draw.line(
      _VARS['surf'], BLACK,
      (0 + PADLEFTRIGHT, 0 + PADTOPBOTTOM),
      (0 + PADLEFTRIGHT, HEIGHT - PADTOPBOTTOM), 2)
    # RIGHT TOP TO BOTTOM
    pygame.draw.line(
      _VARS['surf'], BLACK,
      (WIDTH - PADLEFTRIGHT, 0 + PADTOPBOTTOM),
      (WIDTH - PADLEFTRIGHT, HEIGHT - PADTOPBOTTOM), 2)

    # Get cell size
    horizontal_cellsize = (WIDTH - (PADLEFTRIGHT*2))/divisions
    vertical_cellsize = (HEIGHT - (PADTOPBOTTOM*2))/divisions

    # VERTICAL DIVISIONS: (0,1,2) for grid(3) for example
    for x in range(divisions):
        pygame.draw.line(
           _VARS['surf'], BLACK,
           (0 + PADLEFTRIGHT+(horizontal_cellsize*x), 0 + PADTOPBOTTOM),
           (0 + PADLEFTRIGHT+horizontal_cellsize*x, HEIGHT - PADTOPBOTTOM), 2)
    # HORITZONTAL DIVISION
        pygame.draw.line(
          _VARS['surf'], BLACK,
          (0 + PADLEFTRIGHT, 0 + PADTOPBOTTOM + (vertical_cellsize*x)),
          (WIDTH - PADLEFTRIGHT, 0 + PADTOPBOTTOM + (vertical_cellsize*x)), 2)


def checkEvents():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == KEYDOWN and event.key == K_q:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN and event.key == K_d:
            draw_circ(0,0,20)
            pygame.display.flip()



if __name__ == '__main__':
    main()