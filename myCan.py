class LeftBank:
    def __init__(self,m,c):
        self.mis = m
        self.can = c

class RightBank:
    def __init__(self,m,c):
        self.mis = 3-m
        self.can = 3-c

class Boat:
    def __init__(self):
        self.inLeft = True
        self.mis = 0
        self.can = 0

class State:
    def __init__(self,m,c,b):
        self.boat_inLeft = b
        self.leftBank = LeftBank(m,c)
        self.rightBank = RightBank(m,c)
        self.mis = m
        self.can = c
        self.child = []
        # self.parent = None

    def isValid(self):
        l,r = True, True
        if (self.mis < 0 or self.can < 0):
            l = False
        if (not self.boat_inLeft and self.leftBank.mis != 0 and self.leftBank.mis < self.leftBank.can):
            l = False
        if (self.boat_inLeft and self.rightBank.mis != 0 and self.rightBank.mis < self.rightBank.can):
            r = False
        return (l and r)


    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False


# initial_state,final_state = [[3,3,True],[0,0,True]],[[0,0,False],[0,0,False]]
initial_state = State(3,3,True)
final_state = State(0,0,False)
states = [initial_state]
all_states = [initial_state]

def nextStates(current_state):
    if (current_state.boat_inLeft):
        print "Boat in left"
        m = current_state.leftBank.mis
        c = current_state.leftBank.can
        a = -1
    else:
        print "Boat in right"
        m = current_state.rightBank.mis
        c = current_state.rightBank.can 
        a = 1
    print (m,c)
    for i in range(m+1):
        for j in range(c+1):
            if (i+j > 2 or i+j <= 0):
                continue
            else:
                next_state = State(current_state.leftBank.mis + i * a,current_state.leftBank.can + j * a, not current_state.boat_inLeft)
                if (next_state.isValid() and (any(x != next_state) for x in all_states)):
                    # print (next_state.mis,next_state.can, next_state.boat_inLeft)
                    current_state.child.insert(0,next_state)
                    # next_state.parent = current_state
                    #states.insert(0,next_state)
    for child in current_state.child:
        states.insert(0,child)
        all_states.append(child)
        # print(child.mis,child.can,child.boat_inLeft)

                # else:
                #     next_state = State(current_state.leftBank.mis+i,current_state.leftBank.can + j, not current_state.boat_inLeft)
                #     if (next_state not in all_states and next_state.mis >= next_state.can):
                #         current_state.child.insert(0,next_state)
                #         next_state.parent = current_state
                #         states.insert(0,next_state)

    # else:
    #     print ("Boat in Right")
    #     m = current_state.rightBank.mis
    #     c = current_state.rightBank.can
    #
    #     for i in range(m+1):
    #         for j in range(c+1):
    #             if (i+j > 2 or i+j == 0):
    #                 continue
    #             else:
    #                 next_state = State(current_state.leftBank.mis+i,current_state.leftBank.can + j, not current_state.boat_inLeft)
    #                 if (next_state.leftBank.mis >= next_state.leftBank.can and next_state.rightBank.mis  >= next_state.rightBank.can and next_state not in all_states):
    #                     current_state.child.insert(0,next_state)
    #                     next_state.parent = current_state
    #                     states.insert(0,next_state)

    for i in states:
        print (i.mis,i.can,i.boat_inLeft)
        print ("************************")
    #     # for j in i.child:
    #     #     print (j.mis,j.can,j.boat_inLeft)
    # print ("***************************")


while(True):
    new_state = states.pop()
    # print (new_state.mis,new_state.can,new_state.boat_inLeft)
    if (new_state.mis == final_state.mis and new_state.can == final_state.can and new_state.boat_inLeft == final_state.boat_inLeft):
        print ("Solution")
        break
    # if (len(new_state.child) > 0):
    #     for i in new_state.child:
    #         states.insert(0,i)
    nextStates(new_state)

for i in all_states:
    print (i.mis,i.can,i.boat_inLeft)
