from game import *
from MyPriorityQueue import *

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

  # def bestFirst(self, state, depth=1):
  #   frontier = PriorityQueue()
  #   explored = set()
    
  #   start = Node(state)
  #   frontier.put(start)

  #   self.game.board.printBoard()
  #   for i in range(depth):
  #     if(frontier.empty()): return None

  #     next = frontier.get()
  #     explored.add(next)
  #     children = self.expand(next)
  #     children.sort(key = lambda x: -x.value)
  #     best = children[0]
  #     self.game.setState(best)
  #     self.game.board.printBoard()
  #     best.printState()

  #     # print(next.getState(), "->", best.getState())
  #     inExplored = best.state in explored
  #     inFrontier = frontier.has(best)
  #     if (not inExplored and not inFrontier):
  #       frontier.put(best)
  #     elif(inFrontier): frontier.update(best)
  #     self.game.nextTurn()
    
  #   self.game.setState(start)

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
      self.game.setState(best)
      if (self.game.done()): return best

      for node in nodesAtLevel:
        frontier.remove(node)
        if (self.verbosity > 1): node.printState("removed")

        explored.add(node)
        self.game.setState(node)
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


  def minmax(self):
    pass

  def prune(self):
    pass

  def simulate(self):
    game = self.game
    startingTurn = game.turn

    self.maxDepth = 5
    # self.uniformcost(game.getState(),self.maxDepth)
    # for i in range(self.maxDepth):
    best = self.bestFirst(game.getState(),10)
    print('')
    printPath(best)
      # best.printState()
    
    # p = PriorityQueue()
    # p.put(Node("you", 10))
    # p.put(Node("hey", 3))
    # p.put(Node("your", 6))
    # p.printQueue()

    # p.update(Node("hey", 7))
    # print(p.get())
    # print(p.get())
    # print(p.get())
    # p.printQueue()
    

    # print(p.getList())
    # p.put((-11, "there"))

    # print(p.get()[1])

    # p.remove(Node("hey"))
    # p.printQueue()
    # currentState = State(game.getState())
    # best = self.dfsExpand(currentState)

    # for elem in list(self.open.queue):
    #   print(elem)

    # print(currentState)
    # self.explored.add(starting)
    # self.open.remove()
    # for x in xrange(0,8):
    #   pass
      # self.greedy()
      # best = 
      # if (self.verbosity > 0): best.printState("chosen:")
      # game.move(best.position)
      # game.printCurrent(self.verbosity)
      

        # game.printCurrent()
    # bestState.printState()
    # starting.printState()
