import re

def getTerms(query):
  m = re.compile('\w+\([\w,*\s*]+\)')
  return m.findall(query)

def getOperators(query):
  m = re.compile('[&&=>]+')
  return m.findall(query)

def getPredicate(x):
  return x[0:x.find('(')]

def unknownPos(arguments):
  positions = []
  for i in xrange(len(arguments)):
    if len(arguments[i]) == 1:
      positions.append(i)
  return positions

def sameKnown(args1, args2, positions):
  if (len(args1) != len(args2)): return False
  if (len(args1) == 0): return True
  for p in positions:
    if args1[p] != args2[p]: return False
  return True

def lastReversedSub(subs):
  if len(subs) == 0: return []
  last = subs[len(subs)-1]
  last = (last[1], last[0])
  return [last]

def allButLastSub(subs):
  if len(subs) <= 1: return []
  return subs[0: len(subs)-1]

def knownPos(arguments):
  positions = []
  for i in xrange(len(arguments)):
    if len(arguments[i]) > 1:
      positions.append(i)
  return positions

def hasUnknown(x):
  unknown = False
  for i in x:
    if (len(i) == 1): return True
  return False

def getArguments(x):
  l = x.find('(')+1
  u = x.find(')')
  args = x[l:u].split(",")
  final = []
  for i in args:
    final.append(i.strip())
  return final

def replaceArgument(term, x, y):
  l = term.find('(')+1
  u = term.find(')')
  return term[0:l] + term[l:u].replace(x, y) + term[u:len(term)]

class Atomic(object):
  def __init__(self, sentence):
    self.sentence = sentence
    self.pred = getPredicate(self.sentence)
    self.args = getArguments(self.sentence)
    self.known = not hasUnknown(self.args)

  def subInArgs(self, sub):
    for a in self.args:
      if (sub[1] == a):
        return True
    return False

  def adjustSubs(self, subs):
    for i in xrange(len(subs)):
      s = subs[i]
      if self.subInArgs(s):
        temp = (s[0], s[1]+"1")
        # subs[i] = temp
        # print('would have changed: ' + str(s) +" into " + str(temp))

  def applySubs(self, subs):
    self.adjustSubs(subs)
    for s in subs:
      for i in xrange(len(self.args)):
        a = self.args[i]
        if (a == s[0]): self.args[i] = s[1]
    self.update()

  def applySubsUnknown(self, subs):
    self.adjustSubs(subs)
    for s in subs:
      for i in xrange(len(self.args)):
        a = self.args[i]
        if (a == s[0] and len(s[0]) == 1):
          self.args[i] = s[1]
    self.update()

  def update(self):
    nargs = len(self.args)
    self.sentence = self.pred + "("
    for i in xrange(nargs-1):
      self.sentence = self.sentence + self.args[i] + ","
    self.sentence = self.sentence + self.args[nargs-1] + ")"

class Sentence(object):
  def __init__(self, sentence):
    self.extractSentence(sentence)

  def extractSentence(self, sentence):
    self.sentence = sentence.replace(" ", "")
    self.ops = getOperators(self.sentence)
    self.parts = []
    self.terms = getTerms(self.sentence)
    self.variables = self.getVariables()
    for t in self.terms:
      self.parts.append(Atomic(t))
    
    self.known = True
    for i in self.parts:
      if hasUnknown(i.args): self.known = False

    self.implication = self.sentence.find("=>") is not -1
    self.atomic = len(self.terms) is 1

  def getVariables(self):
    variables = set()
    for p in self.parts:
      for a in p.args:
        variables.add(a)
    return variables

  def getConsequent(self):
    return self.sentence.split("=>")[1]

  def keyValue(self):
    x = self.sentence

    if self.implication:
      y = x.split("=>")
      z = y[0].split("&&")

      keyTerm = y[1].strip()
      key = getPredicate(keyTerm)
      antecedent = y[0].strip()
      variables = getArguments(keyTerm)

      return key, (antecedent, variables)

    else:
      key = getPredicate(x)
      if self.known: return key, getArguments(x)
      else: return key, None

  def updateSentence(self):
    # nTerms = len(self.terms)
    sentence = self.terms[0]
    for i in xrange(len(self.ops)):
      sentence = sentence + self.ops[i] + self.terms[i+1]

    self.extractSentence(sentence)

  def applySubs(self, subs):
    for i in xrange(len(self.parts)):
      p = self.parts[i]
      p.applySubs(subs)
      self.terms[i] = p.sentence
    self.updateSentence()

  def subUnknown(self, subs):
    for i in xrange(len(self.parts)):
      p = self.parts[i]
      p.applySubsUnknown(subs)
      self.terms[i] = p.sentence
    self.updateSentence()

  def cleanUnknown(self):
    for i in xrange(len(self.terms)):
      t = self.terms[i]
      args = getArguments(t)
      for a in args:
        if (len(a) == 1):
          self.terms[i]= replaceArgument(self.terms[i], a, "_")
    self.updateSentence()

  def __str__(self):
    return self.sentence
    