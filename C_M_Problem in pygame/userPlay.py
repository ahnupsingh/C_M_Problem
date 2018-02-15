import sys, pygame
from pygame.locals import *
pygame.init()

size = width,height = 1200, 670
background = pygame.image.load('river.jpg')
background = pygame.transform.scale(background,size)
screen = pygame.display.set_mode(size, HWSURFACE | DOUBLEBUF | RESIZABLE)
pygame.display.set_caption("Missionaries and Cannibals Problem")
myfont = pygame.font.SysFont('Comic Sans MS', 24)
jerry = pygame.image.load('jerry.png')
jerry = pygame.transform.scale(jerry, (70, 90))
tom = pygame.image.load('tom.png')
tom = pygame.transform.scale(tom,(120,140))
drone = pygame.image.load('drone.png')
drone = pygame.transform.scale(drone,(180,180))

Back_color = 235, 255, 255
red, blue, green, black = (255,0,0), (0,0,255), (0,255,0), (0,0,0)
FPS = 160
# stateSprite = pygame.sprite.Group()
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
        offset = 60
        for i in range(c):
            self.rect = screen.blit(tom,(self.position[0] + offset,self.position[1] - 30))
            offset += 30
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

class State:
    def __init__(self,m_state,c_state,b_state):
        self.index = -1
        self.children = []
        self.m_state = m_state
        self.c_state = c_state
        self.boat_state = b_state
        self.isVisited = False
        self.tot_state = [self.m_state,self.c_state, self.boat_state]

    def update(self,mis,can,b):
        if b:
            self.m_state -= mis
            self.c_state -= can
        else:
            self.m_state += mis
            self.c_state += can
        self.boat_state = b
        self.tot_state = [self.m_state,self.c_state, self.boat_state]

class StatePic(pygame.sprite.Sprite):
    def __init__(self):
        super(StatePic, self).__init__()
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

gameOver = False
state = State(3,3,0)
a = 0
b = BoatPic(0,0,True)
c = 0
leftBank = LeftBank()
rightBank = RightBank()
mis,can = 0,0
while True:
    screen.blit(background,(0,0))
    fpsClock.tick(FPS)
    if gameOver:
        textSurface = myfont.render("||||||||Game Over|||||||||",False,(0,1,0))
        screen.blit(textSurface,(width/2 - textSurface.get_width()/2, height/3- textSurface.get_height()/2))
        a = 0
    if b.position[0]== 170:
        a = 0
        b.inLeft = True
    if b.position[0] == width -250:
        a = 0
        b.inLeft = False

    #   For drawing purpose
    if rightBank.mis == 3 and rightBank.can == 3:
        mis,can = 0,0
        textSurface = myfont.render("Mission Completed",False,(0,1,0))
        b.rect = screen.blit(textSurface,(width/2 - textSurface.get_width()/2, height/3- textSurface.get_height()/2))

    statepic = StatePic()
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            if mis+can < 2:
                if b.inLeft:
                    leftBank.can -= 1
                    if leftBank.can >= 0:
                        can += 1
                else:
                    rightBank.can -= 1
                    if rightBank.can >= 0:
                        can += 1
        if keys[pygame.K_s]:
            if can > 0:
                can -= 1
                if b.inLeft:
                    leftBank.can += 1
                else:
                    rightBank.can += 1
        if keys[pygame.K_z]:
            if mis + can < 2:
                if b.inLeft:
                    leftBank.mis -= 1
                    if leftBank.mis >= 0:
                        mis += 1
                else:
                    rightBank.mis -= 1
                    if rightBank.mis >= 0:
                        mis += 1

        if keys[pygame.K_x]:
            if mis > 0:
                mis -= 1
                if b.inLeft:
                    leftBank.mis += 1
                else:
                    rightBank.mis += 1
        if keys[pygame.K_RIGHT]:
            if mis + can > 0:
                a = 1
                state.update(mis,can,not state.boat_state)
            if (leftBank.mis > 0 and leftBank.can > leftBank.mis) or (rightBank.mis > 0 and rightBank.can > rightBank.mis):
                gameOver = True
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == VIDEORESIZE:
            screen = pygame.display.set_mode(event.dict['size'], HWSURFACE | DOUBLEBUF | RESIZABLE)
            # screen.blit(pygame.transform.scale(jerry, event.dict['size']), (0, 0))
    b.draw(mis,can)
    if a == 1:
        b.update()
    statepic.draw(leftBank,rightBank)
    pygame.display.flip()
    pygame.display.update()
