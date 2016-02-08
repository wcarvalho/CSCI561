from game import *
from MyPriorityQueue import *

INFINITY = 1e10

class AI(object):
  def __init__(self, data, aglorithm, verbosity):
    self.game = Game(data)
    self.maxDepth = 1
    # self.explored = set()
    # self.frontier = PriorityQueue()
    self.aglorithm = aglorithm
    self.verbosity = verbosity

  def expand(self, expand, watch=False):
    game = self.game
    board = game.board
    game.setState(expand)

    availableMoves = list(type(board.openPositions)(board.openPositions))
    availableMoves.sort()

    cpi = game.currentPlayerIndex();    # current player index
    states = []
    for move in availableMoves:
      game.sampleMove(move)
      if (watch): value = game.evaluateBoard(cpi)
      else: value = game.evaluateBoard(1)
      state = Node(game.getState(), value, move)
      if (self.verbosity > 2): state.printState()
      states.append(state)
      game.setState(expand)
    
    return states

  def terminal(self, test):
    self.game.setState(test)
    return self.game.done()

  def bestFirst(self, state, depth=1):
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

      
      if (self.verbosity > 1): print('best path:')
      if (self.verbosity > 1): printPath(frontier.peek())
      self.game.nextTurn()

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
      if (child.value > node.value): node.value = child.value
    else: 
      if (child.value < node.value): node.value = child.value

  def bestChild(self, node, traversal, maxDepth, depth):
    self.game.nextTurn()
    if (maxDepth == depth):
      self.addToMinTraversal(traversal, node)
      return node.value
    
    node.value = -INFINITY
    node.depth = depth
    max = (depth % 2) == 0
    children = self.expand(node)
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
      self.game.nextTurn()
      child.value = self.bestChild(child, traversal, maxDepth, depth + 1)
      self.game.previousTurn()
      self.childComparison(max, node, child)
      self.addToMinTraversal(traversal, child)

    self.game.previousTurn()
    return node.value

  def addToMinTraversal(self, traversal, node):
    traversal.append(type(node)(node, node.value, node.position, node.depth))

  def minimax(self, state, maxDepth=1):
    if (maxDepth == 0): return Node(state)
    traversal = []

    start = Node(state)
    self.addToMinTraversal(traversal, start)
    max = True

    children = self.expand(start)
    for child in children:
      child.value = self.bestChild(child, traversal, maxDepth, 1)
      self.childComparison(max, start, child)
      self.addToMinTraversal(traversal, child)

    self.addToMinTraversal(traversal, start)
 
    return sorted(children, key = lambda x: -x.value)[0], traversal

  def addToPruneTraversal(self, traversal, node):
    # print(node.getPruneState())
    traversal.append(type(node)(node, node.value, node.position, node.depth, type(node.ab)(node.ab)))

  def pruneExplore(self, node, traversal, maxDepth, depth):
    self.game.nextTurn()

    currentIsMax = (depth % 2) == 0
    childIsMax = not currentIsMax

    if(currentIsMax): node.value = node.alpha()
    else: node.value = node.beta()
    node.depth = depth

    children = self.expand(node)

    # if you're at node right before the leaves, return min/max or child
    end = (depth + 1 == maxDepth) or self.terminal(children[0])
    if (end):
      # print('end')
      self.game.previousTurn()
      return self.pruneExploreLeaves(node, children, traversal, depth) 

    else:
      # initialize non leaf children
      for child in children:
        if (childIsMax): child.value = node.beta()
        else: child.value = node.alpha()

      # parse children
      for child in children:
        if (currentIsMax):
          if (node.value > node.beta()): break
        else:
          if (node.value < node.alpha()): break

        passab(node, child)
        value = self.pruneExplore(node, traversal, maxDepth, depth)

        # propogate maximum or minimum values up from leaf
        if(currentIsMax): alphaUpdate(value, node, child)
        else: betaUpdate(value, node, child)

    self.game.previousTurn()
    return node.value

  def pruneExploreLeaves(self, node, children, traversal, parentDepth):

    parentIsMax = (parentDepth%2) == 0

    self.addToPruneTraversal(traversal, node)
    
    for i in range(len(children)):
      child = children[i]
      if (i > 0):
        if (parentIsMax):
          if(node.value > node.beta()): break
          if (node.value > node.alpha()):
            node.setAlpha(node.value)
        else:
          if(node.value < node.alpha()): break
          if (node.value < node.beta()):
            node.setBeta(node.value)
        self.addToPruneTraversal(traversal, node)
      
      passab(node, child)
      child.depth = parentDepth + 1

      if (parentIsMax):
        if (child.value > node.alpha()):
          node.value = child.value
      else: 
        if (child.value < node.beta()):
          node.value = child.value

      self.addToPruneTraversal(traversal, child)
    self.addToPruneTraversal(traversal, node)
    return node.value

  def prune(self, state, maxDepth=1):
    if (maxDepth == 0): return Node(state)

    traversal = []
    root = Node(state)
    children = self.expand(root)
    ab = [-INFINITY, INFINITY]

    # DEPTH 1
    for child in children:
      self.addToPruneTraversal(traversal, root)

      if (root.value > root.beta()): break

      passab(root, child)
      value = self.pruneExplore(child, traversal, maxDepth, 1)
      alphaUpdate(value, root, child)

    self.addToPruneTraversal(traversal, root)

    return sorted(children, key = lambda x: -x.value)[0], traversal

  def simulate(self):
    game = self.game
    startingTurn = game.turn
    self.maxDepth = 2

    # best, traversal = self.minimax(game.getState(),self.maxDepth)
    # best = self.bestFirst(game.getState(),self.maxDepth)
    best, traversal = self.prune(game.getState(), self.maxDepth)
    string = getPruneTraversalString(traversal)
    # print string
    # for i in traversal:
    #   node = i
    #   # print(node.position, node.depth, node.value)
    #   print(node.position, node.depth, node.value, node.ab)
    # for i in traversal:
    #   node = i[0]
    #   print(node.position, node.depth, node.value, i[1], i[2])
    # printPath(best)

def passab(node, child):
  child.ab[0] = node.ab[0]
  child.ab[1] = node.ab[1]

def betaUpdate(value, node, child):
  if (value > child.value): child.value = value
  if (child.value > node.value): node.value = child.value
  if (node.value > node.alpha()): node.setAlpha(node.value)

def alphaUpdate(value, node, child):
  if (value > child.value): child.value = value
  if (child.value > node.value): node.value = child.value
  if (node.value > node.alpha()): node.setAlpha(node.value)

def getPruneTraversalString(traversal):
  string = ""
  for node in traversal:
    string = node.getPruneState() + "\n"
  return string


