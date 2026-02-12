# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
from game import Directions
from typing import List

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()




def tinyMazeSearch(problem: SearchProblem) -> List[Directions]:
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem) -> List[Directions]:
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    #My comments is the pseudocode from the textbook, I'm using it to guide the implementation
    #initialize the frontier using the initial state of problem
    initState = problem.getStartState() #Initial state of the problem
    frontier = util.Stack() #This just straight up creates a stack data structure for us to use as the frontier

    #Now we initialize the explored set to be empty
    exploredSet = set()
    frontier.push((initState, []))
    
    #loop do
    while frontier.isEmpty() == False:
        #choose a leaf node and remove it from the frontier
        state, path = frontier.pop()
        #if the node contains a goal state then return the corresponding solution
        if problem.isGoalState(state): return path
        #add the node to the explored set
        if exploredSet.__contains__(state) == False: 
            exploredSet.add(state)
            for successor, action, stepCost in problem.getSuccessors(state):
                newPath = path + [action]
                frontier.push((successor, newPath))

    util.raiseNotDefined()

def breadthFirstSearch(problem: SearchProblem) -> List[Directions]:
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    #We initialize the frontier and explored set in the same way, but swap the LIFO stack for a FIFO queue
    #The implementation is QUITE LITERALLY the exact same as BFS just swap the util from stack to queue.
    initState = problem.getStartState()
    frontier = util.Queue()

    #Init empty explored set
    exploredSet = set()
    frontier.push((initState, []))

    #loop do
    while frontier.isEmpty() == False:
        #Since queue is FIFO, pop here always grabs the shallowest node to expand
        state, path = frontier.pop()
        #Check if node is the solution state
        if problem.isGoalState(state):
            return path
        #Else, check if node is already visisted before
        if exploredSet.__contains__(state) == False:
            #If never visited before then:
            exploredSet.add(state)
            for successor, action, stepCost in problem.getSuccessors(state):
                newPath = path + [action]
                frontier.push((successor, newPath))
        
    util.raiseNotDefined()

def uniformCostSearch(problem: SearchProblem) -> List[Directions]:
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    #Essentially Dijkstra's algorithm, we just need to use a priority queue and add the cost of the path to the frontier
    #Referenced the format of the textbook (Artificial Intelligence: A Modern Approach)
    #Referenced util.py, so I used the PriorityQueue() function to create a priority queue data structure, then use update() to add items to the frontier.
    
    #Create a node with with a state, and should have a cost of 0.
    startState = problem.getStartState()
    startNode = (startState, [], 0)  #tuple of (state, path, cost)
    
    #The frontier is a priority queue ordered by the cost of the path.
    frontier = util.PriorityQueue()  #utilizing the priority queue data structure from util.py
    frontier.push(startNode, 0)      #The cost of the start node is 0

    #Creating an empty set for explored nodes
    exploredSet = set() 

    bestCost = {startState: 0} #So we can properly replace the frontier

    while frontier.isEmpty() == False:
        #Choose the node in the frontier with the lowest total cost and remove it from the frontier.
        state, path, cost = frontier.pop() #Since it's a priority queue, pop the node with the lowest cost

        #If the node contains a goal state then return the corresponding solution
        if problem.isGoalState(state):
            return path
        
        #Add the node to the explored set
        if exploredSet.__contains__(state) == False:   ##The same thing as saying "if state not in exploredSet:"
            exploredSet.add(state)

            # for each action in problem.ACTIONS(node.STATE)
            for successor, action, stepCost in problem.getSuccessors(state):
                newPath = path + [action]
                newCost = cost + stepCost

                # if child not explored OR cheaper path found
                if exploredSet.__contains__(successor) == False:
                    if successor not in bestCost or newCost < bestCost[successor]:
                        bestCost[successor] = newCost
                        frontier.push((successor, newPath, newCost), newCost)
    
    return [] #No solution found, return empty list.

    ##util.raiseNotDefined()

def nullHeuristic(state, problem=None) -> float:
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic) -> List[Directions]:
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
