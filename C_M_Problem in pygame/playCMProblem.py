# -------------------------------------------------------------
#                       By: Anup Kumar Singh
#                           Prastab Dhakal
#                       CE 4th Year/ 1st Sem
# -------------------------------------------------------------
from index import *


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
        # print("Solution")
        done = True
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

#   To draw each node and its children in the screen
def draw(node):
    if len(node.children) > 0:
        for i in range(len(node.children)):
            x_pos, y_pos = node.x_pos + 90, node.y_pos + (i-len(node.children)/2) * 90
            node.children[i].setPos(x_pos,y_pos)
            pygame.draw.line(screen,blue,(node.x_pos,node.y_pos),(x_pos,y_pos),1)
            pygame.draw.circle(screen,red,(x_pos,y_pos),10,9)
            textSurface = myfont.render("(" + str(node.children[i].m_state) + "," + str(node.children[i].c_state) + "," + str(node.children[i].boat_state) + ")",False,(0,1,0))
            screen.blit(textSurface,(x_pos-textSurface.get_width()/2 , y_pos + textSurface.get_height()/2))
            draw(node.children[i])

def drawTree():
    screen = pygame.display.set_mode(size)
    while True:
        screen.fill(Back_color)
        fpsClock.tick(FPS)
    #   Draw root node in the screen
        nodes[0].setPos(75,height/2)
        pygame.draw.circle(screen,red,(nodes[0].x_pos,nodes[0].y_pos),10)
        textSurface = myfont.render("(" + str(nodes[0].m_state) + "," + str(nodes[0].c_state) + "," + str(nodes[0].boat_state) + ")",False,(0,1,0))
        screen.blit(textSurface,(nodes[0].x_pos-textSurface.get_width()/2 , nodes[0].y_pos + textSurface.get_height()/2))
        draw(nodes[0])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        pygame.display.flip()
        pygame.display.update()

stack = [nodes[0]]
sol_stack = [nodes[0]]
def solutionPath():
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

def Simulate():
    b = BoatPic(0,0,True)
    c = 0
    leftBank.update(3,3)
    rightBank.update(0,0)
    screen = pygame.display.set_mode(size)
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

def playGame():
    screen = pygame.display.set_mode(size)
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
        textSurface = myfont.render("A: TOM up S: TOM down",False,(0,1,0))
        screen.blit(textSurface,(width/2 - textSurface.get_width()/2,50))
        textSurface = myfont.render("Z: JERRY up X: JERRY down RIGHT: Go",False,(0,1,0))
        screen.blit(textSurface,(width/2 - textSurface.get_width()/2,80))
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

while True:
    screen.fill(Back_color)
    textSurface = myfont.render("Welcome to the Missionaries and Cannibals Problem",False,(0,1,0))
    screen.blit(textSurface,(width/2-textSurface.get_width()/2 , height/2 - textSurface.get_height()/2))
    textSurface = myfont.render("By: Anup Kumar Singh and Prastab Dhakal",False,(0,1,0))
    screen.blit(textSurface,(width/2-textSurface.get_width()/2 , height/2 + textSurface.get_height()/2))

    screen.blit(pygame.transform.flip(arrow,True,False),(20,height/2-arrow.get_height()/2))
    textSurface = myfont.render("Simulation",False,(0,1,0))
    screen.blit(textSurface,(100,height/2-textSurface.get_height()/2))
    screen.blit(arrow,(width - arrow.get_width()-20,height/2- arrow.get_height()/2))
    textSurface = myfont.render("Tree",False,(0,1,0))
    screen.blit(textSurface,(width - textSurface.get_width()-100,height/2- textSurface.get_height()/2))
    screen.blit(d_arrow,(width/2-arrow.get_width()/4,height-arrow.get_height()/2-250))
    textSurface = myfont.render("Play Game",False,(0,1,0))
    screen.blit(textSurface,(width/2 - textSurface.get_width()/2,height - textSurface.get_height()-20))

    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            solutionPath()
            Simulate()
        if keys[pygame.K_RIGHT]:
            drawTree()
        if keys[pygame.K_DOWN]:
            playGame()
        if event.type == pygame.QUIT:
            sys.exit()
    pygame.display.flip()
    pygame.display.update()
