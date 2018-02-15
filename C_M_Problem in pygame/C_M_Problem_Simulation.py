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

initial_state,final_state = [[3,3,True],[0,0,True]],[[0,0,False],[3,3,False]]
queue = [initial_state]
data = []

state = State(initial_state[0][0], initial_state[0][1], initial_state[0][2])
state.index = 0

leftBank = LeftBank()
rightBank = RightBank()
boat = Boat()

root_state = state
parent_state = state

state_queue = [parent_state]
nodes = [parent_state]

def set_original_value(leftBank,rightBank,boat,m,c):
    boat.inLeft = not boat.inLeft
    if boat.inLeft == True:
        leftBank.mis += m
        leftBank.can += c
        rightBank.mis -= m
        rightBank.can -= c
    else:
        rightBank.mis += m
        rightBank.can += c
        leftBank.mis -= m
        leftBank.can -= c

while True:
    current_state = queue.pop(0)
    current_parent_state = state_queue.pop(0)

    if (current_state[0][1] > current_state[0][0] and current_state[0][0] != 0) or (current_state[1][1] > current_state[1][0] and current_state[1][0] != 0):
        #print("Invalid Condition")
        continue
    if (current_state == final_state):
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RIGHT]:
                break
        break
    leftBank.mis,leftBank.can = current_state[0][0],current_state[0][1]
    rightBank.mis, rightBank.can = current_state[1][0],current_state[1][1]
    boat.inLeft = current_state[0][2]

    mis_travel,can_travel = -1 ,-1

#   Possible Number of missionaries or cannibals to travel
    if (boat.inLeft == True):
        mis_travel = (2 if leftBank.mis >2 else leftBank.mis)
        can_travel = (2 if leftBank.can >2 else leftBank.can)
    else:
        mis_travel = (2 if rightBank.mis >2 else rightBank.mis)
        can_travel = (2 if rightBank.can >2 else rightBank.can)

    for m in range(mis_travel + 1):
        for c in range(can_travel + 1):
            if (m+c >2 or m+c == 0):
                continue
            boat.mis = m
            boat.can = c

            if boat.inLeft == True:      # boat is in the left bank
                leftBank.mis -= m
                leftBank.can -= c
                rightBank.mis += m
                rightBank.can += c
            else:                        # boat is in the right bank
                leftBank.mis += m
                leftBank.can += c
                rightBank.mis -= m
                rightBank.can -= c
            boat.inLeft = not(boat.inLeft)
            this_state = [[leftBank.mis, leftBank.can, boat.inLeft],[rightBank.mis, rightBank.can, boat.inLeft]]

            if (this_state not in data):
                if (this_state not in queue):
                    queue.append(this_state)

                    temp_state = State(this_state[0][0],this_state[0][1],this_state[0][2])
                    temp_state.index = current_parent_state.index + 1
                    current_parent_state.children.append(temp_state)
                    state_queue.append(temp_state)
                    nodes.append(temp_state)
            set_original_value(leftBank,rightBank,boat,m,c)
    data.append(current_state)

stack = [nodes[0]]
sol_stack = [nodes[0]]
state = nodes[0]

while (state.tot_state != [0,0,False]):
    if len(state.children) != 0 and state.isVisited == False:
        a = 0
        for states in state.children:
            if states.isVisited == False:
                a = 1
                stack.append(states)
        if a == 0:
            state.isVisited == True
            stack.pop()
            sol_stack.pop()
            sol_stack.pop()

    else:
        state.isVisited = True
        stack.pop()
        sol_stack.pop()
    sol_stack.append(stack[len(stack)-1])
    state = sol_stack[len(sol_stack)-1]

del queue[:]
del state_queue[:]
del nodes[:]
del data[:]

b = BoatPic(0,0,True)
c = 0
leftBank.update(3,3)
rightBank.update(0,0)

while True:
    screen.blit(background,(0,0))
    fpsClock.tick(FPS)

    #   For drawing purpose
    if c == 11:
        mis,can = 0,0
        textSurface = myfont.render("Mission Completed",False,(0,1,0))
        b.rect = screen.blit(textSurface,(b.position[0], b.position[1] - textSurface.get_height()/2))
    else:
        mis = abs(sol_stack[c].m_state - sol_stack[c+1].m_state)
        can = abs(sol_stack[c].c_state - sol_stack[c+1].c_state)

    if sol_stack[c].boat_state:
        leftBank.update(sol_stack[c].m_state-mis,sol_stack[c].c_state-can)
    else:
        rightBank.update(3-sol_stack[c].m_state-mis,3-sol_stack[c].c_state-can)
    statepic = StatePic()
    if b.position[0] == 170 or b.position[0] == width - 250:
        if c == 11:
            c = 11
        else:
            c+= 1
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            c += 1
        if keys[pygame.K_LEFT]:
            c -= 1
            if c < 0:
                c = 0
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == VIDEORESIZE:
            screen = pygame.display.set_mode(event.dict['size'], HWSURFACE | DOUBLEBUF | RESIZABLE)
            # screen.blit(pygame.transform.scale(jerry, event.dict['size']), (0, 0))
    statepic.draw(leftBank,rightBank)
    b.draw(mis,can)
    b.update()
    pygame.display.flip()
    pygame.display.update()
