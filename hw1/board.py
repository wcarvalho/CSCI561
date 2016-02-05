class Board(object):
  def __init__(self, input, start):
    end = self.setBoardValues(input, start)
    self.setStartingPositions(input, end)
    self.readOpenPositions()
    self.boardWidth = len(self.values[0])

  def setBoardValues(self, input, start):
    i = start
    self.values = []
    while (True):
      if (input[i][0] == "*"): break
      if (input[i][0] == "O"): break
      if (input[i][0] == "X"): break
      self.values.append(map(int, input[i].split()))
      i = i +1
    return i

  def setStartingPositions(self, input, i):
    self.positions = []
    while(i < len(input)):
      positions_i = []
      for x in (input[i]):
        positions_i.append(x)
      self.positions.append(positions_i)
      i = i + 1
  
  def readOpenPositions(self):
    self.openPositions = set()
    for i in range(len(self.positions)):
      row = self.positions[i]
      for j in range(len(row)):
        if (self.positions[i][j] == "*"):
          self.openPositions.add((i,j))

  def printOpen(self): print("board open:", self.openPositions)

  def printBoard(self):
    for row in self.positions:
      print("".join(row))

  def getState(self):
    state = ""
    for i in range(len(self.positions)):
      row = self.positions[i];
      for j in range(len(row)):
        state = state + row[j]
    return state 

  def setState(self, state):
    for i in range(len(state)):
      row = i/self.boardWidth
      column = i%self.boardWidth
      self.positions[row][column] = state[i]
    self.readOpenPositions()

  def add(self, position): self.openPositions.add(position)

  def remove(self, position): self.openPositions.remove(position)

  def getOpen(self): return next(iter(self.openPositions))

  def getNeighbors(self, position):
    row, col = position
    left = (row, col-1)
    up = (row - 1, col)
    right = (row, col+1)
    down = (row+1, col)
    neighbors = [left, up, right, down]
    toremove = []
    for i,j in neighbors:
      height = len(self.positions)
      width = self.boardWidth
      if (i < 0 or j < 0 or i >= height or j >= width): 
        toremove.append((i,j))

    for i in toremove:
      neighbors.remove(i)
      
    return neighbors