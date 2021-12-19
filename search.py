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


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
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

    nosAExplorar = util.Stack()
    nosExplorados = []

    caminhosNos = dict()
    caminhosNos[problem.getStartState()] = []

    nosAExplorar.push(problem.getStartState())

    while not(nosAExplorar.isEmpty()):
        noAtual = nosAExplorar.pop()

        if (problem.isGoalState(noAtual)):
            return caminhosNos[noAtual]

        nosExplorados.append(noAtual)

        infosFilhosNoAtual = problem.getSuccessors(noAtual)

        for infosFilho in infosFilhosNoAtual:
            if (infosFilho[0] not in nosExplorados):
                acoes = caminhosNos[noAtual].copy()
                acoes.append(infosFilho[1])

                nosAExplorar.push(infosFilho[0])
                caminhosNos[infosFilho[0]] = acoes
                   
    return []


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    
    nosAExplorar = util.Queue()
    nosExplorados = []

    caminhosNos = dict()
    caminhosNos[problem.getStartState()] = []

    nosAExplorar.push(problem.getStartState())

    while not(nosAExplorar.isEmpty()):
        noAtual = nosAExplorar.pop()

        if (problem.isGoalState(noAtual)):
            return caminhosNos[noAtual]
        
        nosExplorados.append(noAtual)

        infosFilhosNoAtual = problem.getSuccessors(noAtual)

        for infosFilho in infosFilhosNoAtual:

            estaNaQueue = False

            for no in nosAExplorar.list:
                if infosFilho[0] == no:
                    estaNaQueue = True
                    break
                
            if (infosFilho[0] not in nosExplorados and not(estaNaQueue)):
                acoes = caminhosNos[noAtual].copy()
                acoes.append(infosFilho[1])

                nosAExplorar.push(infosFilho[0])
                caminhosNos[infosFilho[0]] = acoes
                   
    return []


def uniformCostSearch(problem):
    """Search the node of least total cost first."""

    nosAExplorar = util.PriorityQueue()
    nosExplorados = []

    caminhoCustoNos = dict()

    nosAExplorar.push(problem.getStartState(), 0.0)
    caminhoCustoNos[problem.getStartState()] = [[], 0.0]

    while (not nosAExplorar.isEmpty()):
        noAtual = nosAExplorar.pop()

        if (noAtual not in nosExplorados):
            if (problem.isGoalState(noAtual)):
                return caminhoCustoNos[noAtual][0]

            nosExplorados.append(noAtual)
                
            infosFilhosNoAtual = problem.getSuccessors(noAtual)

            for infosFilho in infosFilhosNoAtual:

                estaNaPQueue = False
                custoNaPQueue = infosFilho[2]

                for no in nosAExplorar.heap:
                    if infosFilho[0] == no[2]:
                        estaNaPQueue = True
                        custoNaPQueue = caminhoCustoNos[no[2]][1]
                        break

                custoCaminho = caminhoCustoNos[noAtual][1] + infosFilho[2]    

                if infosFilho[0] not in nosExplorados and not(estaNaPQueue):
                    acoes = caminhoCustoNos[noAtual][0].copy()
                    acoes.append(infosFilho[1])

                    nosAExplorar.push(infosFilho[0], custoCaminho)
                    caminhoCustoNos[infosFilho[0]] = [acoes, custoCaminho]

                elif estaNaPQueue and custoNaPQueue > custoCaminho:

                    for no in nosAExplorar.heap:
                        if infosFilho[0] == no[2]:
                            caminhoCustoNos[no[2]][1] = custoCaminho

                            acoes = caminhoCustoNos[noAtual][0].copy()
                            acoes.append(infosFilho[1])
                            caminhoCustoNos[no[2]][0] = acoes

                            nosAExplorar.update(infosFilho[0], custoCaminho)
                   
    return []



def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def greedySearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest heuristic first."""

    nosAExplorar = util.PriorityQueue()
    nosExplorados = []

    caminhoNos = dict()

    nosAExplorar.push(problem.getStartState(), heuristic(problem.getStartState(), problem))
    caminhoNos[problem.getStartState()] = []

    while (not nosAExplorar.isEmpty()):
        noAtual = nosAExplorar.pop()

        if (noAtual not in nosExplorados):
            if (problem.isGoalState(noAtual)):
                return caminhoNos[noAtual]

            nosExplorados.append(noAtual)
            
            infosFilhosNoAtual = problem.getSuccessors(noAtual)

            for infosFilho in infosFilhosNoAtual:

                estaNaPQueue = False

                for no in nosAExplorar.heap:
                    if infosFilho[0] == no[2]:
                        estaNaPQueue = True
                        break
                
                if infosFilho[0] not in nosExplorados and not(estaNaPQueue):
                    acoes = caminhoNos[noAtual].copy()
                    acoes.append(infosFilho[1])
                    nosAExplorar.push(infosFilho[0], heuristic(infosFilho[0], problem))

                    caminhoNos[infosFilho[0]] = acoes
                   
    return []


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""

    nosAExplorar = util.PriorityQueue()
    nosExplorados = []

    caminhoCustoNos = dict()

    nosAExplorar.push(problem.getStartState(), 0.0 + heuristic(problem.getStartState(), problem))
    caminhoCustoNos[problem.getStartState()] = [[], 0.0]

    while (not nosAExplorar.isEmpty()):
        noAtual = nosAExplorar.pop()

        if (noAtual not in nosExplorados):
            if (problem.isGoalState(noAtual)):
                return caminhoCustoNos[noAtual][0]
            
            nosExplorados.append(noAtual)
            
            infosFilhosNoAtual = problem.getSuccessors(noAtual)

            for infosFilho in infosFilhosNoAtual:

                estaNaPQueue = False
                custoNaPQueue = infosFilho[2]

                for no in nosAExplorar.heap:
                    if infosFilho[0] == no[2]:
                        estaNaPQueue = True
                        custoNaPQueue = caminhoCustoNos[no[2]][1]
                        break

                custoCaminho = caminhoCustoNos[noAtual][1] + infosFilho[2]
                
                if infosFilho[0] not in nosExplorados: 
                    if not(estaNaPQueue):
                        acoes = caminhoCustoNos[noAtual][0].copy()
                        acoes.append(infosFilho[1])
                        nosAExplorar.push(infosFilho[0], custoCaminho + heuristic(infosFilho[0], problem))
                        
                        caminhoCustoNos[infosFilho[0]] = [acoes, custoCaminho]

                    elif estaNaPQueue and custoNaPQueue > custoCaminho:
                        for no in nosAExplorar.heap:
                            if infosFilho[0] == no[2]:
                                caminhoCustoNos[no[2]][1] = custoCaminho

                                acoes = caminhoCustoNos[noAtual][0].copy()
                                acoes.append(infosFilho[1])
                                caminhoCustoNos[no[2]][0] = acoes

                                nosAExplorar.update(infosFilho[0], custoCaminho + heuristic(infosFilho[0], problem))
                   
    return []


def foodHeuristic(state, problem):
    """
    Your heuristic for the FoodSearchProblem goes here.

    This heuristic must be consistent to ensure correctness.  First, try to come
    up with an admissible heuristic; almost all admissible heuristics will be
    consistent as well.

    If using A* ever finds a solution that is worse uniform cost search finds,
    your heuristic is *not* consistent, and probably not admissible!  On the
    other hand, inadmissible or inconsistent heuristics may find optimal
    solutions, so be careful.

    The state is a tuple ( pacmanPosition, foodGrid ) where foodGrid is a Grid
    (see game.py) of either True or False. You can call foodGrid.asList() to get
    a list of food coordinates instead.

    If you want access to info like walls, capsules, etc., you can query the
    problem.  For example, problem.walls gives you a Grid of where the walls
    are.

    If you want to *store* information to be reused in other calls to the
    heuristic, there is a dictionary called problem.heuristicInfo that you can
    use. For example, if you only want to count the walls once and store that
    value, try: problem.heuristicInfo['wallCount'] = problem.walls.count()
    Subsequent calls to this heuristic can access
    problem.heuristicInfo['wallCount']
    """
    position, foodGrid = state

    listaFoodGrid = foodGrid.asList()

    distancias = []

    for i in range(len(listaFoodGrid)):
        distancias.append(util.manhattanDistance(position, listaFoodGrid[i]))

    if len(listaFoodGrid) == 0:
        return 0
    else:
        return sum(distancias)/len(listaFoodGrid)

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
ucs = uniformCostSearch
gs = greedySearch
astar = aStarSearch
