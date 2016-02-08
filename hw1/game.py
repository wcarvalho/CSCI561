from board import *
from player import *

class Game(object):
  def __init__(self, data):
    self.task = int(data[0])
    self.turn = 0
    
    if (self.task < 4): 
      self.setupSinglePlayer(data)
    else: 
      self.setupMultiPlayer(data)
    
  def setupSinglePlayer(self, data):
    self.board = Board(data,3)
    self.players = [ Player(self.board, "X"), Player(self.board, "O")]
    if (data[1] == "O"): self.players.reverse()
    

  def setupMultiPlayer(self, data):
    self.board = Board(data,7)

  def evaluateBoard(self, which): 
    player = self.players[(which - 1 )% 2]
    value_player = 0
    for i,j in player.takenPositions:
      value_player = value_player + self.board.values[i][j]

    opponent = self.players[which % 2]
    value_opponent = 0
    for i,j in opponent.takenPositions:
      value_opponent = value_opponent + self.board.values[i][j]

    return value_player - value_opponent

  def setPosition(self, position, player):
    i, j = position
    board = self.board
    if (board.positions[i][j] == "*"):
      board.remove(position)

    board.positions[i][j] = player.which
    self.currentPlayer().add(position)

  def currentPlayerIndex(self): 
    return 1 + (self.turn % 2)
  def otherPlayerIndex(self): 
    return 2-(1 + self.currentPlayerIndex())%2
  
  def currentPlayer(self): return self.players[self.turn % 2]
  def otherPlayer(self): return self.players[(self.turn + 1) % 2]  

  def move(self, position, increase=True):
    player = self.players[self.turn % 2]
    if player.hasAlly(position): 
      self.raid(position, player)
    else: 
      self.sneak(position, player)
    if (increase): self.turn = self.turn + 1

  def raid(self, position, player):
    self.setPosition(position, player)
    board = self.board
    neighbors = board.getNeighbors(position)

    for i, j in neighbors:
      if (board.positions[i][j] == player.enemy):
        self.setPosition((i,j), player)
        self.otherPlayer().remove((i,j))


  def sneak(self, position, player):
    self.setPosition(position, player)

  def printCurrent(self, verbosity=0):
    if (verbosity >= 1):
      self.board.printBoard()
      if (verbosity > 2):
        self.board.printOpen()
        print(self.currentPlayer().printTaken())
        print(self.otherPlayer().printTaken())
        print('')

  def nextTurn(self): self.turn = self.turn+1
  def previousTurn(self): self.turn = self.turn-1
  def setTurn(self, turn): self.turn = turn

  def sampleMove(self, position):
    # self.printCurrent()
    startState = self.board.getState()
    self.move(position, False)
    # self.printCurrent()
    
    return startState

  def getState(self): return self.board.getState()

  def setState(self, state):
    self.board.setState(state)
    for player in self.players:
      player.readBoard()

  def done(self): return len(self.board.openPositions) == 0