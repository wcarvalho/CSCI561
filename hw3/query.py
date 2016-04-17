import sys

def argmapToList(orderedArgs, map):
  list = []
  for i in orderedArgs:
    if not i in map: continue
    v = map[i]
    if v == True: list.append("+")
    else: list.append("-")
  return list

def parseArguments(args):
  table = {}
  for a in args:
    s = a.find("=")
    if (s > -1):
      pre = a[:s-1].strip()
      post = a[s+1:len(a)].strip()
      table[pre] = post == "+" and True or False
    else:
      table[a] = None
    #   if post == "+": table[pre] = True
    #   elif post == "-": table[pre] = False
    # else: table[pre] = None

  return table

def getOrderedArgumentList(args):
  ordered = []
  for a in args:
    s = a.find("=")
    if (s > -1):
      pre = a[:s-1].strip()
      ordered.append(pre)
    else:
      ordered.append(a)
  return ordered

def makeArgStr(map, arg):
  if arg not in map: return arg
  elif map[arg] == True: return arg + " = +" 
  elif map[arg] == False: return arg + " = -" 
  else: return arg

def bayesRule(pre, post, map):
  # non_ancestors = list(set(args) - set(ancestors))
  top1 = constructJoint(pre+post, map)
  # top2 = constructJoint(ancestors, map)
  bottom = constructJoint(post, map)
  return top1, bottom

def constructConditional(map, pre, post):
  str = "P("
  if (len(pre)>0):
    for a in pre[:len(pre)-1]:
      str = str + makeArgStr(map, a) + ", "
    str = str + makeArgStr(map, pre[len(pre)-1]) + " | "
  if (len(post)>0):
    for a in post[:len(post)-1]:
      str = str + makeArgStr(map, a) + ", "
    str = str + makeArgStr(map, post[len(post)-1]) + ")"
  else: str = str + ")"

  return str

def constructUtilityQuery(args, map):
  utilityQuery = constructConditional(map, ["utility = +"], args)
  # utilityQuery=utilityQuery.replace("P(", "EU(")
  return utilityQuery

def constructJoint(args, map):
  str = "P("
  for a in args[:len(args)-1]:
    str = str + makeArgStr(map, a) + ", "
  str = str + makeArgStr(map, args[len(args)-1]) + ")"
  return str

class Query(object):
  def __init__(self, query):
    self.type="P"
    self.str = query
    self.conditionalArgs = []
    self.argTypes = []
    self.arguments = {}
    self.args = []
    self.parseQuery(query)

  def parseQuery(self, query):
    l = query.find("(")
    self.getType(query[:l])
    self.getArgumentTypes(query[l+1:])
    self.getArguments(query[l+1:])

  def getArgumentTypes(self,arg):
    if arg.find("|") > -1: 
      self.argTypes.append("C")
    # if: self.argType = "J"

  def conditional(self): return "C" in self.argTypes 

  def getUnknowns(self):
    unknown = []
    for i in self.arguments:
      if self.arguments[i] == None:
        unknown.append(i)
    return unknown

  def getArguments(self, arg):
    if self.conditional():
      b = arg.find("|")
      pre = map(str.strip, arg[:b].split(","))
      post = map(str.strip, arg[b+1:arg.find(")")].split(","))
      preTable = parseArguments(pre)
      postTable = parseArguments(post)
      self.arguments.update(preTable)
      self.arguments.update(postTable)
      self.args = self.args + preTable.keys() + postTable.keys()
      self.conditionalArgs = self.conditionalArgs+ preTable.keys()

    else:
      args = map(str.strip, arg[:len(arg)-1].split(","))
      oargs = getOrderedArgumentList(args)
      argTable = parseArguments(args)
      self.arguments.update(argTable)
      self.args = self.args + oargs

  def setArguments(self, argMap):
    for i in argMap:
      if i in self.arguments:
        self.arguments[i] = argMap[i]
    pre, post = self.getPrePost()
    if self.conditional(): self.str = constructConditional(self.arguments, pre, post)
    else: self.str = constructJoint(self.arguments.keys(), self.arguments)
    # self.str = self.str.replace("P(", self.type +"(")
  
  def getPrePost(self):
    pre = self.conditionalArgs
    post = list(set(self.arguments.keys()) - set(pre))
    return pre,post
  def setMarginal(self):
    self.argTypes.append("M")
  def getType(self, prefix):
    if prefix == "P": self.type = "P"
    elif prefix == "EU": self.type = "EU"
    elif prefix == "MEU": self.type = "MEU"

  def pp(self):
    print self.str
    print "Type: " + self.type
    print "ArgTypes: " + str(self.argTypes)
    print "\t"+str(self.arguments)
    print "\tconditional: " + str(self.conditionalArgs)
    # for i in self.arguments:
    #   print "\t" + i + ": " + str(self.arguments[i])