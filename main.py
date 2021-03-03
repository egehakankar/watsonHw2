# coding=utf-8
# This is the submission of the project group named WATSON for Homework 2.
# To run normally: python main.py

# Members:
#           Mehmet Berk Şahin (CONTACT)
#           Balaj Saleem
#           Mehmet Alper Genç
#           Ege Hakan Karaağaç
#           Fırat Yönak

import random
import sys
import plotly.graph_objects as go
import plotly.offline as pyo
import plotly as py
import numpy as np
from copy import deepcopy
import random


# State is a 4x4 array
# moves are left right top bottom

# beam first search:
# check the lowest


# initializs the goal locations / points for each number
def getGoalStateLocations():

    """
      This is function generates a list of lists, which contain the tuples contains the locations where each number should be in the goal state

      Returns:
      Returns the final locations of all numbers in goal state
    """


    locations = []
    locations.append([(3, 3)])  # 0s
    locations.append([(0, 0)])  # 1s
    locations.append([(0, 1), (1, 0), (2, 3), (3, 2)])  # 2s
    locations.append([(0, 2), (1, 1), (1, 3), (2, 0), (2, 2), (3, 1)])  # 3s
    locations.append([(0, 3), (1, 2), (2, 1), (3, 0)])  # 4s
    return locations


def printPuzzle(puz, puzName):
     
    """
      This is function generates the figure for the puzzle visualization

      Parameters:
      puz: the state that is to be visualized
      puzName: the name of the puzzle figure

      Returns:
      Returns the figure of the puzzle
    """

    fig = go.Figure(data=[go.Table(
        header=dict(
            values=[[puzName],
                    ['0'],
                    ['1'],
                    ['2'],
                    ['3']],
            fill_color='royalblue',
            line_color='darkslategray',
            font=dict(color='white')),
        cells=dict(values=[
            [0, 1, 2, 3],
            [puz[0][0], puz[1][0], puz[2][0], puz[3][0]],
            [puz[0][1], puz[1][1], puz[2][1], puz[3][1]],
            [puz[0][2], puz[1][2], puz[2][2], puz[3][2]],
            [puz[0][3], puz[1][3], puz[2][3], puz[3][3]]],
            fill=dict(color=['royalblue', 'white', 'white', 'white', 'white']),
            line_color='darkslategray',
            font=dict(color=['white', 'black', 'black', 'black', 'black'])))
    ])
    fig.update_layout(autosize=False, width=400, height=325)

    return fig


def randomPuzzleGenerator(goalState):
    
    """
      This is function generates the a random puzzle state starting from the goal state

      Parameters:
      goalState: the state that is to shuffled to obtain the final state

      Returns:
      Returns the shuffled state, which is solvable
    """
    directions = ['u', 'd', 'l', 'r']
    forbidden_directions = []
    variation_val=10
    new_state = goalState
    for i in range(variation_val):
        zero_loc = getZeroLocation(new_state)
        forbidden_directions.clear()
        if (zero_loc[0] == 0):
            forbidden_directions.append('u')
        if (zero_loc[0] == 3):
            forbidden_directions.append('d')
        if (zero_loc[1] == 0):
            forbidden_directions.append('l')
        if (zero_loc[1] == 3):
            forbidden_directions.append('r')

        direction = random.choice(directions)
        while (direction in forbidden_directions):
            direction = random.choice(directions)

        new_state = move_zero(new_state, zero_loc[0], zero_loc[1], direction)
    return new_state


def goalStateGenerater():
    
    """
      This is function generates the goal state

      Parameters:

      Returns:
      Returns the fully arranged goal state
    """

    w = 4
    goal = [[0 for x in range(w)] for y in range(w)]
    goal[0][0] = 1
    goal[0][1], goal[1][0], goal[2][3], goal[3][2] = 2, 2, 2, 2
    goal[0][2], goal[1][1], goal[1][3], goal[2][0], goal[2][2], goal[3][1] = 3, 3, 3, 3, 3, 3
    goal[0][3], goal[1][2], goal[2][1], goal[3][0] = 4, 4, 4, 4
    return goal


def getZeroLocation(state):
    return np.array(np.where(np.array(state) == 0)).T.flatten()


def hamDist(state, goalLocs):

    """
      This is the heuristic function for cumulative hamming distance of the state. 
      This basically calculates how many tiles are not in their ideal / goal location.
      The higher this value the further we are from the goal state.

      Parameters:
      state: The state where to apply this heuristic function on
      goalLocs: The final / ideal locations of each tile in goal state

      Returns:
      Returns the total hamming distance
    """

    totalDistance = 0
    for i in range(4):
        for j in range(4):
            num = state[i][j]
            if ((i, j) not in goalLocs[num]):
                totalDistance = totalDistance + 1
    return totalDistance

def move_zero(state, i, j, direction):

    """
      This function moves zero in a specified direction of up down left right

      Parameters:
      state: The state in which the zero is to be moved
      i: The row location of zero
      j: The column location of zero
      direction: the direction to move the zero in

      Returns:
      Returns the final state after the directional change is applied
    """
    return_state = deepcopy(state)
    if direction == 'u':
        return_state[i][j], return_state[i - 1][j] = return_state[i - 1][j], return_state[i][j]
        i = i - 1
    if direction == 'd':
        return_state[i][j], return_state[i + 1][j] = return_state[i + 1][j], return_state[i][j]
        i = i + 1
    if direction == 'l':
        return_state[i][j], return_state[i][j - 1] = return_state[i][j - 1], return_state[i][j]
        j = j - 1
    if direction == 'r':
        return_state[i][j], return_state[i][j + 1] = return_state[i][j + 1], return_state[i][j]
        j = j + 1
    return return_state


def beamer(initState, goalState, goalLocs, w=1):

    """
      This function performs beam search consitently incremeting w, starting from w = 2

      Parameters:
      initState : The starting state from where to start the beam search
      goalState: The final state that the algorithm seems to find
      goalLocs: The final location of elements in the goal state
      w: the beam widht

      Returns:
      Returns whether or not the solution was found, set of moves performed to reach the goal state and the value of final W
    """

    found = False
    currState = initState
    available = []  # stores available nodes and their H value
    h = hamDist(currState, goalLocs)
    available.append((currState, h))
    closed = []  # stores the closed nodes and their H value
    state_history = []
    moves = []
    while (not found):
        w = w + 1
        available.clear()
        closed.clear()
        state_history.clear()
        moves.clear()
        h = hamDist(initState, goalLocs)
        available.append((initState, h))
        while (available):

            if (len(available) > 10000):
                break

            currState, h = available.pop(0)
            if (currState == goalState):
                found = True
                child = goalState
                moves = getMovesFromAllStates(state_history, initState, goalState)
                break

            if (currState in closed):
                continue

            # h = hamDist(currState, goalLocs)
            # available.remove( (currState, h) )
            closed.append(currState)
            zero_loc = getZeroLocation(currState)
            # check all available new states
            new_states = []
            if (zero_loc[0] > 0):
                next_state = move_zero(currState, zero_loc[0], zero_loc[1], 'u')
                next_h = hamDist(next_state, goalLocs)
                if (next_state not in closed):
                    new_states.append((next_state, next_h))
                    state_history.append((currState, next_state))
            if (zero_loc[0] < 3):
                next_state = move_zero(currState, zero_loc[0], zero_loc[1], 'd')
                next_h = hamDist(next_state, goalLocs)
                if (next_state not in closed):
                    new_states.append((next_state, next_h))
                    state_history.append((currState, next_state))
            if (zero_loc[1] > 0):
                next_state = move_zero(currState, zero_loc[0], zero_loc[1], 'l')
                next_h = hamDist(next_state, goalLocs)
                if (next_state not in closed):
                    new_states.append((next_state, next_h))
                    state_history.append((currState, next_state))
            if (zero_loc[1] < 3):
                next_state = move_zero(currState, zero_loc[0], zero_loc[1], 'r')
                next_h = hamDist(next_state, goalLocs)
                if (next_state not in closed):
                    new_states.append((next_state, next_h))
                    state_history.append((currState, next_state))
                    # get the top w new states
            new_states.sort(key=lambda tup: tup[1])
            available.extend(new_states[0:w])  # add the w two best states to available

            # available.sort(key=lambda tup: tup[1]) #sort available, so we go for the best option in next iteration

    moves.reverse()
    return found, moves, w


def trace_states(states):
    """
      This function traces / prints an array of states in an orderly fashion

      Parameters:
      states: a set of states 

      Returns:
      
    """
    print('STATE HISTORY:')
    for state in states:
        print("----------------")
        print(np.array(state))


def findParent(state_history, child):
    """
      This function finds the parent of a child state

      Parameters:
      state_history : The state history, i.e set of states and their parents visited by beam search
      child: the node whos parent needs to be found  

      Returns:
      Returns the parent state of the child node
    """
    for item in state_history:
        if (item[1] == child):
            return item[0]
    return None


def getMovesFromAllStates(state_history, initState, goalState):


    """
      This function performs gets the set of moves performed to reach a solution

      Parameters:
      state_history : The state history, i.e set of states and their parents visited by beam search
      goalState  : The State array that the algorithm aims to find.
      initState  : The State array that the algorithm begun with.

      Returns:
      Returns a list of states representing the path between the start and
      goal states.
    """

    moves = []
    child = goalState
    moves.append(child)
    print(f"Len: {len(state_history)}")
    parent = findParent(state_history, child)
    # find the chain in state history
    while (parent != initState):
        temp = child
        child = parent
        parent = findParent(state_history, temp)
        moves.append(parent)

    res = []
    [res.append(x) for x in moves if x not in res]
    return res


goal = goalStateGenerater()
goalLocs = getGoalStateLocations()
print("Goal State:")
print(np.array(goal))

S1 = randomPuzzleGenerator(goal)
S2 = randomPuzzleGenerator(goal)
S3 = randomPuzzleGenerator(goal)

print("S1 Initial State:")
print(np.array(S1))
print("S2 Initial State:")
print(np.array(S2))
print("S3 Initial State:")
print(np.array(S3))

found, moves1, w1 = beamer(S1, goal, goalLocs)
trace_states(moves1)
print(f"total moves: {len(moves1)}, W: {w1}")
found, moves2, w2 = beamer(S2, goal, goalLocs)
trace_states(moves2)
print(f"total moves: {len(moves2)}, W: {w2}")
found, moves3, w3 = beamer(S3, goal, goalLocs)
trace_states(moves3)  # moves array contains all the states that lead upto the solution
print(f"total moves: {len(moves3)}, W: {w3}")



# The lines of code below prints the results of the algorithms into the p_graph.html file generated by this program.
# It first shows the goal state in a table. Then, it moves on to the results for the 3 randomly generated initial states.
# Firstly, it prints out the sum of the beam widths of all solutions. Then, for each solution, the program first prints 
# out the beam width of the solution, and the number of moves in the solution. Then, it prints out the initial state 
# followed by the current state after each move.
# After printing out all solutions, the program prints the sum of w's one la


allPlots = []
goal1 = printPuzzle(goal, "Goal")
initState1 = printPuzzle(goal, "Init S1")
initState2 = printPuzzle(goal, "Init S2")
initState3 = printPuzzle(goal, "Init S3")
allPlots.append(goal1)
f = open("p_graph.html", "w")
f.write("<h1> Goal State:</h1>")
f.write(goal1.to_html(full_html=False, include_plotlyjs='cdn'))
f.write("<h1> Beam Search Results:</h1>")
f.write(f"<h3> Sum of w's: {w1 + w2 + w3}</h3>")
f.write("<hr>")

f.write("<h2> Solution for S1:</h2>")
f.write(f"<h3> w1 = {w1}, Number of moves: {len(moves1) - 1}</h3>")
i = 0
for move in moves1:
    move_g = printPuzzle(move, ("Initial State S1: ")) if i == 0 else printPuzzle(move, ("S1 move: " + str(i)))
    allPlots.append(move_g)
    f.write(move_g.to_html(full_html=False, include_plotlyjs='cdn'))
    i = i + 1

f.write("<hr>")
f.write("<h2> Solution for S2:</h2>")
f.write(f"<h3> w2 = {w2}, Number of moves: {len(moves2) - 1}</h3>")
i = 0
for move in moves2:
    move_g = printPuzzle(move, ("Initial State S2: ")) if i == 0 else printPuzzle(move, ("S2 move: " + str(i)))
    allPlots.append(move_g)
    f.write(move_g.to_html(full_html=False, include_plotlyjs='cdn'))
    i = i + 1

f.write("<hr>")
f.write("<h2> Solution for S3:</h2>")
f.write(f"<h3> w3 = {w3}, Number of moves: {len(moves3) - 1}</h3>")
i = 0
for move in moves3:
    move_g = printPuzzle(move, ("Initial State S3: ")) if i == 0 else printPuzzle(move, ("S3 move: " + str(i)))
    allPlots.append(move_g)
    f.write(move_g.to_html(full_html=False, include_plotlyjs='cdn'))
    i = i + 1

f.write("<hr>")
f.write(f"<h3> Sum of w's: {w1 + w2 + w3}</h3>")
print("Sum of w's: " + str(w1 + w2 + w3))
f.close()
exit(0)
