import sys, pygame
from pygame.locals import *
pygame.init()

size = width,height = 1200, 670
screen = pygame.display.set_mode(size, HWSURFACE | DOUBLEBUF | RESIZABLE)
pygame.display.set_caption("Missionaries and Cannibals Problem")
myfont = pygame.font.SysFont('Comic Sans MS', 24)

background = pygame.image.load('river.jpg')
background = pygame.transform.scale(background,size)
pygame.display.set_caption("Missionaries and Cannibals Problem")
myfont = pygame.font.SysFont('Comic Sans MS', 24)
jerry = pygame.image.load('jerry.png')
jerry = pygame.transform.scale(jerry, (70, 90))
tom = pygame.image.load('tom.png')
tom = pygame.transform.scale(tom,(120,140))
drone = pygame.image.load('drone.png')
drone = pygame.transform.scale(drone,(180,180))
arrow = pygame.image.load('arrow.png')
arrow = pygame.transform.scale(arrow,(240,90))
d_arrow = pygame.transform.rotate(arrow,-90)

Back_color = 235, 255, 255
red = (255,0,0)
blue = (0,0,255)
FPS = 60
fpsClock = pygame.time.Clock()

class LeftBank:
    def __init__(self):
        self.mis = 3
        self.can = 3
    def update(self,m,c):
        self.mis = m
        self.can = c


class RightBank:
    def __init__(self):
        self.mis = 0
        self.can = 0
    def update(self,m,c):
        self.mis = m
        self.can = c


class Boat:
    def __init__(self):
        self.inLeft = True
        self.mis = 0
        self.can = 0

class State:
    def __init__(self,m_state,c_state,b_state):
        self.index = -1
        self.children = []
        self.m_state = m_state
        self.c_state = c_state
        self.boat_state = b_state
        self.isVisited = False
        self.tot_state = [self.m_state,self.c_state, self.boat_state]

    def setPos(self,x_pos,y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos

    def update(self,mis,can,b):
        if b:
            self.m_state -= mis
            self.c_state -= can
        else:
            self.m_state += mis
            self.c_state += can
        self.boat_state = b
        self.tot_state = [self.m_state,self.c_state, self.boat_state]

class BoatPic(pygame.sprite.Sprite):
    def __init__(self, m, c, inLeft):
        super(BoatPic, self).__init__()
        self.x_pos = 200
        if inLeft:
            self.x_pos = 176
        else:
            self.x_pos = width - 250
        self.inLeft = inLeft
        self.speed = [1,0]
        self.position = [self.x_pos, height/3-90]

    def draw(self,m,c):
        offset = 25
        for i in range(c):
            self.rect = screen.blit(tom,(self.position[0] + offset,self.position[1] - 30))
            offset += 50
        for i in range(m):
            self.rect = screen.blit(jerry,(self.position[0] + offset + 20,self.position[1]))
            offset += 30
        if self.inLeft:
            self.rect = screen.blit(drone,self.position)
        else:
            self.rect = screen.blit(pygame.transform.flip(drone,True,False),self.position)

    def update(self):
        if self.position[0] == width - 250:
            self.inLeft = False
        if self.position[0] == 170:
            self.inLeft = True
        if self.inLeft:
            self.position[0] += 2
        else:
            self.position[0] -= 2

class StatePic(pygame.sprite.Sprite):
    def __init__(self):
        super(StatePic, self).__init__()
        # stateSprite.add(self)
        # self.state = node
        # self.inLeft = [node.m_state,node.c_state]
        self.image = pygame.Surface([width,height])
        self.image.fill(Back_color)
        self.rect = self.image.get_rect()

    def draw(self,l,r):
        left,right = 5,120
        for j in range(l.can):
            screen.blit(pygame.transform.flip(tom,True,False),(left,height/2))
            left = left + 90
        for i in range(r.can):
            screen.blit(tom,(width-right,height/2))
            right = right + 90

        left,right = 80,130
        for i in range(l.mis):
            # pygame.draw.circle(screen,blue,(left,height/2),10)
            screen.blit(jerry,(left,height - 260))
            left = left + 90
        for j in range(r.mis):
            # pygame.draw.circle(screen,blue,(width-right,height/2),10)
            screen.blit(pygame.transform.flip(jerry,True,False),(width-right,height - 260))
            right = right + 90
