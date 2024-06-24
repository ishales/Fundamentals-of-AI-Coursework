##############
# Homework 2 #
##############

##############
# Question 1 #
##############

# The code runs through the input FRINGE. First, it converts FRINGE to a list
# so that it can be edited. Then it takes the first element of the list.
# If the first element is not a tuple and stands alone, it is added to the final list.
# Else, the element is added to the back of the list. By using the extend, rather than
# append function here, upon added the tuple element to the back of the list, it is unpacked
# by one level, allowing the BFS to run properly.
# Lastly, the final list of single elements in order is returned. 
def BFS(FRINGE):
    # list to return final node order
    nodes = []
    # turn tuple into a list
    mytree = list(FRINGE)
   
    #look at the first element of the list
    while(len(mytree) > 0):
        curr = mytree.pop(0)
        # if element is single leaf
        if type(curr) != tuple:
            # add element to final list
            nodes.append(curr)           
        else:
            # otherwise add element to back of list (for next round)
            mytree.extend(curr)

    # if you are done searching, return the final list
    return nodes

        
#print(BFS(("ROOT",)))
#print(BFS((((("L", "E"), "F"), "T"))))
#print(BFS((("R", ("I", ("G", ("H", "T")))))))
#print(BFS(((("A", ("B",)), "C", ("D",)))))
#print( BFS((("T", ("H", "R", "E"), "E"))))
#print(BFS((("A", (("C", (("E",), "D")), "B")))))


##############
# Question 2 #
##############


# These functions implement a depth-first solver for the homer-baby-dog-poison
# problem. In this implementation, a state is represented by a single tuple
# (homer, baby, dog, poison), where each variable is True if the respective entity is
# on the west side of the river, and False if it is on the east side.
# Thus, the initial state for this problem is (False False False False) (everybody
# is on the east side) and the goal state is (True True True True).

# The main entry point for this solver is the function DFS, which is called
# with (a) the state to search from and (b) the path to this state. It returns
# the complete path from the initial state to the goal state: this path is a
# list of intermediate problem states. The first element of the path is the
# initial state and the last element is the goal state. Each intermediate state
# is the state that results from applying the appropriate operator to the
# preceding state. If there is no solution, DFS returns [].
# To call DFS to solve the original problem, one would call
# DFS((False, False, False, False), [])
# However, it should be possible to call DFS with a different initial
# state or with an initial path.

# First, we define the helper functions of DFS.

# FINAL-STATE takes a single argument S, the current state, and returns True if it
# is the goal state (True, True, True, True) and False otherwise.
def FINAL_STATE(S):
    if S == (True, True, True, True):
        return True
    else:
        return False


# NEXT-STATE returns the state that results from applying an operator to the
# current state. It takes three arguments: the current state (S), and which entity
# to move (A, equal to "h" for homer only, "b" for homer with baby, "d" for homer
# with dog, and "p" for homer with poison).
# It returns a list containing the state that results from that move.
# If applying this operator results in an invalid state (because the dog and baby,
# or poisoin and baby are left unsupervised on one side of the river), or when the
# action is impossible (homer is not on the same side as the entity) it returns None.
# NOTE that next-state returns a list containing the successor state (which is
# itself a tuple)# the return should look something like [(False, False, True, True)].
def NEXT_STATE(S, A):
    S = list(S)
    h = 1
    b = 2
    d = 3
    p = 4
    
    # move just homer
    if A == h:
        if S[0] == True:
            S[0] = False
        else:
            S[0] = True
    # move baby
    elif A == b:
        if (S[1] == True and S[0] == True):
            S[1] = False
            S[0] = False
        elif (S[1] == False and S[0] == False):
            S[1] = True
            S[0] = True
        else:
            return None

    # move dog
    elif A == d:
        if (S[2] == True and S[0] == True):
            S[2] = False
            S[0] = False
        elif (S[2] == False and S[0] == False):
            S[2] = True
            S[0] = True
        else:
            return None

    # move poison
    elif A == p:
        if (S[3] == True and S[0] == True):
            S[3] = False
            S[0] = False
        elif (S[3] == False and S[0] == False):
            S[3] = True
            S[0] = True
        else:
            return None

    S = tuple(S)

    # check if state is valid
    invalid_s = [ (False, True, True, True), (True, False, False, False),   # homer one one side, everyone else on other
                  (False, True, True, False), (True, False, False, True),   # dog and baby stuck together
                  (False, True, False, True), (True, False, True, False) ]   # baby and poison stuck together
                  
    if S in invalid_s:
        return None
  
    return [S]


# SUCC-FN returns all of the possible legal successor states to the current
# state. It takes a single argument (s), which encodes the current state, and
# returns a list of each state that can be reached by applying legal operators
# to the current state.
def SUCC_FN(S):
    final = []
    h = 1
    b = 2
    d = 3
    p = 4

    hmove = NEXT_STATE(S, h)
    if(hmove != None):
        print("h: ", hmove)
        final += hmove
    
    bmove = NEXT_STATE(S, b)
    if(bmove != None):
        print("b: ", bmove)
        final += bmove
    
    dmove = NEXT_STATE(S, d)
    if(dmove != None):
        print("d: ", dmove)
        final += dmove
    
    pmove = NEXT_STATE(S, p)
    if(pmove != None):
        print("p: ", pmove)
        final += pmove

    return final


# ON-PATH checks whether the current state is on the stack of states visited by
# this depth-first search. It takes two arguments: the current state (S) and the
# stack of states visited by DFS (STATES). It returns True if s is a member of
# states and False otherwise.
def ON_PATH(S, STATES):
    return S in STATES  


# MULT-DFS is a helper function for DFS. It takes two arguments: a list of
# states from the initial state to the current state (PATH), and the legal
# successor states to the last, current state in the PATH (STATES). PATH is a
# first-in first-out list of states# that is, the first element is the initial
# state for the current search and the last element is the most recent state
# explored. MULT-DFS does a depth-first search on each element of STATES in
# turn. If any of those searches reaches the final state, MULT-DFS returns the
# complete path from the initial state to the goal state. Otherwise, it returns
# [].
def MULT_DFS(STATES, PATH):

    print("Current STATES:", STATES)
    print("Current PATH:", PATH)

    for next_s in STATES:
        #look at one state
        print("newNode", next_s)
        # if it isn't the goal, check if we have seen it
        if (ON_PATH(next_s, PATH)):
            print("Already seen:", next_s)
            continue
        # expand curr state
        new_path = PATH + [next_s]
        next_states = SUCC_FN(next_s)
        # if a possible next state is the goal
        for t in next_states:
            if(FINAL_STATE(t)):
               print("Reached goal state:", next_s)
               return new_path + [t]
        return MULT_DFS(next_states, new_path)

     # never got to the goal state
    return []

# DFS does a depth first search from a given state to the goal state. It
# takes two arguments: a state (S) and the path from the initial state to S
# (PATH). If S is the initial state in our search, PATH is set to False. DFS
# performs a depth-first search starting at the given state. It returns the path
# from the initial state to the goal state, if any, or False otherwise. DFS is
# responsible for checking if S is already the goal state, as well as for
# ensuring that the depth-first search does not revisit a node already on the
# search path.
def DFS(S, PATH):

    # initial state case
    if (PATH == False):
        # add current state to path
        PATH = []
        PATH.append(S)
        # check if initial state is goal state
        if (FINAL_STATE(S) == True):
            return PATH

    return MULT_DFS(SUCC_FN(S), PATH)


