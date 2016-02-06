
####### AI
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