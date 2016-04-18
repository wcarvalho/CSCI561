def seperateNameParents(title):
  i = title.find("|")
  if i == -1: return title, []
  else: return title[0:i].strip(), title[i+1:].split()

def seperateKeyValue(row):
  parts = row.split()
  value = float(parts[0])
  parts = map(str.strip, parts[1:])
  key = [True]*len(parts)
  for i in xrange(len(parts)):
    if parts[i] == "-": key[i] = False
  key = [True] + key
  return key, value

def getCompliment(key, value):
  keyp = list(key)
  keyp[0] = False
  valuep = 1.-value
  return keyp, valuep

class Node(object):
  def __init__(self, name, info, verbosity=0):
    self.name = name
    self.argumentMap = {}
    self.ordered_args = []
    self.v = verbosity
    self.P = {}
    self.parents = {}
    self.children = {}
    self.type = "probability"
    self.defineProperties(info)

  def hasParent(self): return len(self.parents) > 0

  def defineArgMap(self, header):
    name, parents = seperateNameParents(header)
    self.ordered_args.append(name)
    self.argumentMap[name] = 0
    for i in xrange(len(parents)):
      self.argumentMap[parents[i]] = i+1
      self.ordered_args.append(parents[i])
    if (len(parents) > 0):
      self.ordered_args = [self.ordered_args[0]] + sorted(self.ordered_args[1:])

  def keyLength(self): return len(self.parents)+1
  def defineProperties(self, info):
    if (self.name == "utility"): self.type = "utility"
    self.defineArgMap(info[0])

    for i in xrange(1, len(info)):
      n = info[i]
      if (i == 0): self.name = n
      else:
        if (n == 'decision'): 
          self.type = "decision"
          return
        key1, value1 = seperateKeyValue(n)
        self.P[tuple(key1)] = value1
        if (value1 != "decision" and self.name != "utility"):
          value1 = float(value1)
          key2, value2 = getCompliment(key1, value1)
          self.P[tuple(key2)] = value2

  def addParent(self, parent):
    self.parents[parent.name] = parent
  def addChild(self, child):
    self.children[child.name] = child
  
  def getValue(self, arguments):
    key = [True]*self.keyLength()

    for i in self.argumentMap:
      indx = self.argumentMap[i]
      key[indx] = arguments[i]

    value = self.P[tuple(key)]

    return value

  def listD(self, dictionary):
    str = ""
    for i in dictionary:
      str = str + dictionary[i].name + " "
    return str
  
  # def listParents(self):
  #   print "\tParents: "
  #   for i in self.parents:
  #     print "\t\t" + self.parents[i].name
  def pp(self):
    print self.name, self.type
    print "\tChildren: " + self.listD(self.children)
    print "\tParents: " + self.listD(self.parents)
    # for i in self.parents:
    #   print "\t\t" + i.name

    # + str(map(Node.name, self.parents)) 
    for i in self.P:
      print "\t" + str(i) + ": " + str(self.P[i])
