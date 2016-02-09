import Queue

INFINITY = 1e10
LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def getPos(pos):
  if (pos[0] == -1): return "root"
  return LETTERS[pos[1]] + str(pos[0]+1)

def intStr(val):
  if (val == -INFINITY): return "-Infinity"
  elif (val == INFINITY): return "Infinity"
  else: return str(val)

def printPath(node):
  q = Queue.LifoQueue()
  while (node != None):
    q.put(node)
    node = node.parent

  print("path:")
  while (not q.empty()):
    q.get().printState("\t")

def getBoardFromState(ai, state):
  originalState = ai.game.getState()
  ai.game.setState(state)
  string = ai.game.board.getBoard()
  ai.game.setState(originalState)
  return string

def getNextFromPath(node):
  if (node.parent == None): return node
  while (True):
    last = node
    node = node.parent
    if (node.parent == None): return last



class Node(object):
  def __init__(self, state, value=-INFINITY, position=(-1,-1), depth=0, alpha =-INFINITY, beta=INFINITY):
    self.state = state
    self.position = position
    self.value = value
    self.depth = depth
    self.parent = None
    self.ab = [alpha, beta]

  def printState(self, arg=""):
    if (len(arg) > 0):
      print(arg + " " + self.getState())
    else:
      print(self.getState())

  def getPos(self):
    if (self.position[0] == -1): return "root"
    return LETTERS[self.position[1]] + str(self.position[0]+1)

  def getState(self):
    end = ", v="+str(self.value) + ", d=" + str(self.depth)
    return self.getPos() + ": " + self.state + end

  def getPruneState(self):
    alpha = self.ab[0]
    beta = self.ab[1]
    return self.getMinimaxState() + "," + intStr(alpha) + "," + intStr(beta)

  def getMinimaxState(self):
    return self.getPos() + "," + str(self.depth) + "," + intStr(self.value)
  
  def __str__(self):
    return self.state;

  def setStart(self, start):
    self.start = start

  def setDepth(self, depth):
    self.depth = depth

  def setParent(self, parent):
    self.parent = parent

  def alpha(self): return self.ab[0]
  def beta(self): return self.ab[1]

  def setAlpha(self, val): self.ab[0] = val
  def setBeta(self, val): self.ab[1] = val
  
class PriorityQueue(Queue.PriorityQueue, object):
  """docstring for PriorityQueue"""
  def __init__(self):
    super(PriorityQueue, self).__init__()

  def remove(self, element):
    stored = []
    while(True):
      latest = self.get()
      if (latest == None): break
      if (latest.state == element.state): break
      stored.append(latest)

    for i in stored:
      self.put(i)

  def has(self, element):
    for i in self.queue:
      if (isinstance(element, Node)):
        if(i[1].state == element.state): return True
      elif (isinstance(element, basestring)):
        if (i[1].state == element): return True
    return False

  def valueOf(self, element):
    for i in self.queue:
      if (i[1].state == element.state):
        return i[1].value
    None

  def update(self, element):
    oldValue = self.valueOf(element)
    newValue = element.value
    if (oldValue == None): put(element)
    if (oldValue < newValue):
      self.remove(element)
      self.put(element)
  
  def put(self, element):
    super(PriorityQueue, self).put((-element.value, element))

  def get(self):
    if (not self.empty()): return self.getValue()[1]
    else: return None

  def getValue(self):
    return super(PriorityQueue, self).get()

  def printQueue(self):
    for i in self.getList():
      i.printState()

  def getList(self):
    list = []
    for i in self.queue:
      list.append(i[1])
    list.sort(key = lambda x: -x.value)
    return list

  def peek(self):
    x = self.get()
    self.put(x)
    return x

  def addList(self, list):
    for i in list:
      self.update(i)