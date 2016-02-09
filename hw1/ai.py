from game import *
from MyPriorityQueue import *
import sys

INFINITY = 1e10

class AI(object):
  def __init__(self, data, verbosity):
    self.game = Game(data)
    self.data = data
    self.task = int(data[0])
    self.verbosity = verbosity

  def setTurnState(self, turn, state):
    self.game.setTurn(turn)
    self.game.setState(state)
  
  def expand(self, expand, watch=False):
    game = self.game
    board = game.board
    game.setState(expand)

    availableMoves = list(type(board.openPositions)(board.openPositions))
    availableMoves.sort()

    cpi = game.currentPlayerIndex();    # current player index
    states = []
    if (self.verbosity > 2): expand.printState(game.currentPlayer().which)
    for move in availableMoves:
      game.sampleMove(move)
      if (watch): value = game.evaluateBoard(cpi)
      else: value = game.evaluateBoard(1)
      state = Node(game.getState(), value, move)
      if (self.verbosity > 2): state.printState("\t->")
      if (self.verbosity > 3): game.board.printBoard(state.state)
      states.append(state)
      game.setState(expand)
    
    return states

  def terminal(self, test):
    self.game.setState(test)
    return self.game.done()

  def bestFirst(self, state, depth=1):
    startingTurn = self.game.turn
    frontier = PriorityQueue()
    explored = set()
    
    frontier.put(Node(state))
    for i in range(depth):
      if(frontier.empty()): return None
      ### current frontier
      if (self.verbosity > 1): print('\n' + str(i) +' ------------------')
      if (self.verbosity > 1): print("current frontier")
      if (self.verbosity > 1): frontier.printQueue()
      
      nodesAtLevel = frontier.getList()

      # test that game is over
      best = frontier.peek()
      if (self.terminal(best)): return best

      for node in nodesAtLevel:
        frontier.remove(node)
        if (self.verbosity > 1): node.printState("removed")

        explored.add(node)
        children = self.expand(node)

        for child in children:
          if (i > 0): child.position = node.position
          child.setParent(node)
          child.setDepth(i+1)
          inExplored = child.state in explored
          inFrontier = frontier.has(child)
          if (not inExplored and not inFrontier):
            frontier.put(child)
          elif(inFrontier): frontier.update(child)

        for child in children:
          if (self.verbosity > 1): child.printState("\t->")

      
      if (self.verbosity > 1): printPath(frontier.peek())
      self.game.nextTurn()

    self.game.setTurn(startingTurn)
    return frontier.get()

  def uniformcost(self, state, depth=1):
    frontier = PriorityQueue()
    explored = set()
    
    frontier.put(Node(state))


    for i in range(depth):
      if(frontier.empty()): return None
      ### current frontier
      if (self.verbosity > 1): print('\n------------------')
      if (self.verbosity > 1): print("current frontier")
      if (self.verbosity > 1): frontier.printQueue()
      
      nodesAtLevel = frontier.getList()

      for node in nodesAtLevel:
        frontier.remove(node)
        if (self.verbosity > 1): node.printState("removed")

        explored.add(node)
        self.game.setState(node)
        children = self.expand(node)
        
        # print('')
        # print(node)
        # print("expanded into")
        for child in children:
          if (self.verbosity > 1): child.printState("\t->")

        for child in children:
          inExplored = child.state in explored
          inFrontier = frontier.has(child)
          if (not inExplored and not inFrontier):
            frontier.put(child)
          elif(inFrontier): frontier.update(child)


      self.game.nextTurn()

  def childComparison(self, max, node, child):
    if (max): 
      # print(node.getPos(), child.value, ">", node.value)
      if (child.value > node.value): node.value = child.value
    else: 
      if (child.value < node.value): node.value = child.value

  def bestChild(self, node, traversal, maxDepth, depth):
    self.game.nextTurn()
    
    node.depth = depth
    max = (depth % 2) == 0
    
    if (depth >= maxDepth):
      self.game.previousTurn()
      return node.value

    children = self.expand(node)
    # if current node is a leaf child, just return it
    if (self.game.done()):
      self.game.previousTurn()
      return node.value
    
    if (max): node.value = -INFINITY
    else: node.value = INFINITY
    # if you're at node right before the leaves, return min/max or child
    end = (depth + 1 == maxDepth) or self.terminal(children[0])
    if (end):
      for child in children:
        child.depth = depth + 1
        self.game.nextTurn()
        self.addToMinTraversal(traversal, node)
        if (node.value == -INFINITY): node.value = child.value
        else: self.childComparison(max, node, child)

        self.game.previousTurn()
        self.addToMinTraversal(traversal, child)
      self.game.previousTurn()
      return node.value

    # if you're at an earlier node, you find the best child value
    for child in children:
      self.addToMinTraversal(traversal, node)
      child.value = self.bestChild(child, traversal, maxDepth, depth + 1)
      self.childComparison(max, node, child)
      self.addToMinTraversal(traversal, child)

    self.game.previousTurn()
    return node.value
  def addToMinTraversal(self, traversal, node):
    traversal.append(node.getMinimaxState())

  def minimax(self, state, maxDepth=1):
    # print('minimax', maxDepth)
    traversal = []
    start = Node(state)
    
    if (maxDepth == 0 or self.game.done()):
      self.addToMinTraversal(traversal, start)
      start.value = self.game.evaluateBoard(1)
      self.addToMinTraversal(traversal, start)
      return start, traversal


    max = True

    children = self.expand(start)
    for child in children:
      self.addToMinTraversal(traversal, start)
      child.value = self.bestChild(child, traversal, maxDepth, 1)
      self.childComparison(max, start, child)
      self.addToMinTraversal(traversal, child)

    self.addToMinTraversal(traversal, start)
    best = sorted(children, key = lambda x: -x.value)[0]
    # best.printState()
    # print(traversal[len(traversal)-1])
    return best, traversal

  def pruneExplore(self, node, traversal, maxDepth, depth):

    self.game.nextTurn()


    children = self.expand(node)
    
    if (depth >= maxDepth or self.game.done()):
      self.game.previousTurn()
      addToPruneTraversal(traversal, node)
      return node.value

    currentIsMax = (depth % 2) == 0
    childIsMax = not currentIsMax

    if(currentIsMax): node.value = node.alpha()
    else: node.value = node.beta()
    node.depth = depth

    # if you're at node right before the leaves, return min/max or child
    end = (depth + 1 == maxDepth) or self.terminal(children[0])
    if (end):
      self.game.previousTurn()
      return self.pruneExploreLeaves(node, children, traversal, depth) 
    else:
      addToPruneTraversal(traversal, node)
      self.pruneGenExplore(node, children, traversal, currentIsMax, maxDepth, depth)
      addToPruneTraversal(traversal, node)
 
    self.game.previousTurn()
    return node.value

  def pruneExploreLeaves(self, node, children, traversal, parentDepth):

    parentIsMax = (parentDepth%2) == 0

    addToPruneTraversal(traversal, node)
    for i in range(len(children)):
      child = children[i]
      if (i > 0):
        if (pruneBranchPass(node, parentIsMax, traversal)): break
      
      passab(node, child)
      child.depth = parentDepth + 1

      if (parentIsMax):
        if (i < len(children)-1):
          if (child.value > node.alpha()):
            node.value = child.value
        else:
          alphaUpdate(child.value, node, child)
      else:
        if (i < len(children)-1):
          if (child.value < node.beta()):
            node.value = child.value
        else: 
          betaUpdate(child.value, node, child)
      addToPruneTraversal(traversal, child)
    addToPruneTraversal(traversal, node)
    return node.value

  def pruneGenExplore(self, node, children, traversal, currentIsMax, maxDepth, depth):
    for i in range(len(children)):
      child = children[i]

      if (i > 0):
        if (pruneBranchPass(node, currentIsMax, traversal)): break

      passab(node, child)
      value = self.pruneExplore(child, traversal, maxDepth, depth+1)
      # propogate maximum or minimum values up from leaf
      if(currentIsMax): alphaUpdate(value, node, child)
      else: betaUpdate(value, node, child)

  def prune(self, state, maxDepth=1):
    # print('prune')
    root = Node(state)
    traversal = []
    
    if (maxDepth == 0 or self.game.done()): 
      addToPruneTraversal(traversal, root)
      root.value = self.game.evaluateBoard(1)
      alphaUpdate(root.value, root, root)
      addToPruneTraversal(traversal, root)
      return root, traversal

    children = self.expand(root)
    addToPruneTraversal(traversal, root)
    depth = 0
    self.pruneGenExplore(root, children, traversal, True, maxDepth, depth)

    addToPruneTraversal(traversal, root)

    return sorted(children, key = lambda x: -x.value)[0], traversal

  def normalSetup(self):
    game = self.game
    startingTurn = game.turn
    startingState = game.getState()
    self.startingPlayer = self.data[1]
    self.maxDepth = int(self.data[2])
    return game, startingTurn, startingState

  def task1(self):
    game, startingTurn, startingState = self.normalSetup()
    best = self.bestFirst(game.getState(),self.maxDepth)
    self.setTurnState(startingTurn, startingState)
    return best

  def task2(self):
    game, startingTurn, startingState = self.normalSetup()
    best, traversal = self.minimax(game.getState(),self.maxDepth)
    self.setTurnState(startingTurn, startingState)
    string = 'Node,Depth,Value\r\n' + getTraversalString(traversal)
    return best, string
  
  def task3(self):
    game, startingTurn, startingState = self.normalSetup()
    best, traversal = self.prune(game.getState(), self.maxDepth)
    self.setTurnState(startingTurn, startingState)
    string = 'Node,Depth,Value,Alpha,Beta\r\n' + getTraversalString(traversal)
    return best, string
  
  def pickMove(self, algorith, maxDepth):
    if (algorith == 1): 
      return getNextFromPath(self.bestFirst(self.game.getState(), maxDepth))
    elif (algorith == 2): 
      return self.minimax(self.game.getState(), maxDepth)[0]
    elif (algorith == 3): 
      return self.prune(self.game.getState(), maxDepth)[0]

  def task4(self):
    game = self.game
    startingTurn = game.turn
    startingState = game.getState()
    
    player1 = self.data[1]
    player1Algo = int(self.data[2])
    player1Depth = int(self.data[3])
    
    player2 = self.data[4]
    player2Algo = int(self.data[5])
    player2Depth = int(self.data[6])

    traversal = ""
    # game.board.printBoard()
    # print()
    while (not game.done()):
      player1Move = self.pickMove(player1Algo, player1Depth)
      game.setState(player1Move)
      game.nextTurn()
      traversal = traversal + game.board.getBoard() + "\r\n"
      # game.board.printBoard()
      # print()
      if (game.done()): break
      
      player2Move = self.pickMove(player2Algo, player2Depth)
      game.setState(player2Move)
      game.nextTurn()
      traversal = traversal + game.board.getBoard() + "\r\n"
      # game.board.printBoard()
      # print()
      # if (game.turn > 2): break

    return traversal

def passab(node, child):
  child.ab[0] = node.ab[0]
  child.ab[1] = node.ab[1]

def pruneBranchPass(node, isMax, traversal):
  if (isMax):
    if(node.value >= node.beta()): return True
    if (node.value > node.alpha()):
      node.setAlpha(node.value)
  else:
    if(node.value <= node.alpha()): return True
    if (node.value < node.beta()):
      node.setBeta(node.value)
  addToPruneTraversal(traversal, node)
  return False

def addToPruneTraversal(traversal, node):
  traversal.append(node.getPruneState())

def betaUpdate(value, node, child):
  if (value < child.value): child.value = value
  if (child.value < node.value): node.value = child.value
  if (node.value < node.beta()): node.setBeta(node.value)

def alphaUpdate(value, node, child):
  if (value > child.value): child.value = value
  if (child.value > node.value): node.value = child.value
  if (node.value > node.alpha()): node.setAlpha(node.value)

def getTraversalString(traversal):
  string = ""
  for i in traversal:
    string = string + i + "\r\n"
  return string
