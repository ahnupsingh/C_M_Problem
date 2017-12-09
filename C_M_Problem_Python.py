class LeftBank:
    def __init__(self):
        self.mis = 3
        self.can = 3

class RightBank:
    def __init__(self):
        self.mis = 0
        self.can = 0

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
    # print(queue)
    current_state = queue.pop(0)
    current_parent_state = state_queue.pop(0)

    if (current_state[0][1] > current_state[0][0] and current_state[0][0] != 0) or (current_state[1][1] > current_state[1][0] and current_state[1][0] != 0):
        # print("Invalid Condition")
        continue
    if (current_state == final_state):
        print("Solution")
        done = True
        break

    leftBank.mis,leftBank.can = current_state[0][0],current_state[0][1]
    rightBank.mis, rightBank.can = current_state[1][0],current_state[1][1]
    boat.inLeft = current_state[0][2]

    mis_travel,can_travel = -1 ,-1

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
            # print (this_state)
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


stack = []
current_node = root_state
current_node.isVisited = True
dfs_buffer = []
tab = 0
while True:
    # print current_node
    # if current_node in dfs_buffer:
    #     print 'hello there'
    if ((current_node not in dfs_buffer) and tab >=0):
        prefix = '      |       '
        suffix = '      |-------'
        # print current_node
        if tab == 0:
            print str(current_node.tot_state)
        if tab > 0:
            print prefix * (tab-1) + suffix + str(current_node.tot_state)
        # print
    if (current_node != None):
        if (x.isVisited == False for x in current_node.children) and len(current_node.children) > 0:
            # print type(x)
            next_node = next(x for x in current_node.children if x.isVisited == False)
            # print str(next_node.tot_state)
            dfs_buffer.append(current_node)
            stack.append(current_node)
            # print next_node == current_node
            next_node.isVisited = True
            current_node = next_node
            # if current_node in dfs_buffer:
            tab += 1
        else:
            current_node = stack.pop()
            tab -= 1
    else:
        break
