from board import *

class Player(object):
  def __init__(self, board, which):
    self.board = board
    self.which = which
    if (which == "X"): self.enemy = "O"
    else: self.enemy = "X"

    self.readBoard()

  def readBoard(self):
    positions = self.board.positions
    self.takenPositions = set()
    for i in range(len(positions)):
      row = positions[i]
      for j in range(len(row)):
        if (positions[i][j] == self.which):
          self.takenPositions.add((i,j))

  def printTaken(self): print("player " + str(self.which) + " taken:", self.takenPositions)

  def currentEvaluation(self):
    for i,j in self.takenPositions:
      print( i, j)

  def add(self, position): self.takenPositions.add(position)

  def remove(self, position): self.takenPositions.remove(position)

  def getAllies(self, position):
    neighbors = self.board.getNeighbors(position)
    allies = []
    for neighbor in neighbors:
      if (neighbor in self.takenPositions):
        allies.append(neighbor)
    
    return allies

  def hasAlly(self, position):
    allies = self.getAllies(position)
    if (len(allies) > 0): return True
    else: return False