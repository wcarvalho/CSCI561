from game import *
from Queue import *

class State(object):
  def __init__(self, string, value=0, position=(-1,-1)):
    self.string = string
    self.position = position
    self.value = value

  def printState(self, arg=""):
    if (len(arg) > 0):
      print(arg, self.string, self.value, self.position)
    else:
      print(self.string, self.value, self.position)

  def __str__(self):
    return self.string;

class AI(object):
  def __init__(self, data, aglorithm, verbosity):
    self.game = Game(data)
    self.explored = set()
    self.open = Queue()
    self.aglorithm = aglorithm
    self.verbosity = verbosity

  def addToOpen(self, states):
    for state in states:
      self.open.put(state)

    states.sort(key=lambda x: -x.value)
    return states[0]

  def bfsExpand(self, expand):
    states = self.expand(expand)
    return self.addToOpen(states)

  def dfsExpand(self, expand):
    states = self.expand(expand)
    states.reverse()
    return self.addToOpen(states)

  def expand(self, expand):
    game = self.game
    board = game.board
    allOpen = type(board.openPositions)(board.openPositions)


    if (expand != game.getState()):
      game.setState(expand.string)

    current_index = game.currentPlayerIndex();
    starting = State(game.getState(), game.evaluateBoard(current_index))
    states = []
    for open in allOpen:
      game.sampleMove(open)
      value = game.evaluateBoard(current_index)
      state = State(game.getState(), game.evaluateBoard(current_index), open)
      if (self.verbosity > 1): state.printState()
      states.append(state)
      game.setState(starting.string)

    self.explored.add(starting)
    
    return states

  def bestfirst(self):
    

  def minmax(self):
    pass


  def prune(self):
    pass

  def simulate(self):
    game = self.game

    currentState = State(game.getState())
    best = self.dfsExpand(currentState)

    for elem in list(self.open.queue):
      print(elem)

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
