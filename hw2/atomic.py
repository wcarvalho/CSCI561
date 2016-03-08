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

def hasUnknown(x):
  unknown = False
  for i in x:
    if (len(i) > 1): pass
    X=i.find('x') is not -1
    Y=i.find('y') is not -1
    Z=i.find('z') is not -1
    unknown = unknown or (X or Y or Z)
  return unknown

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
  # print ("term", term)
  # print ("x", x)
  # print ("y", y)
  return term[0:l] + term[l:u].replace(x, y) + term[u:len(term)]


class Atomic(object):
  def __init__(self, sentence):
    self.sentence = sentence
    self.pred = getPredicate(self.sentence)
    self.args = getArguments(self.sentence)
    self.known = not hasUnknown(self.args)

class Sentence(object):
  def __init__(self, sentence):
    self.extractSentence(sentence)

  def extractSentence(self, sentence):
    self.sentence = sentence.replace(" ", "")
    self.ops = getOperators(self.sentence)
    self.parts = []
    self.terms = getTerms(self.sentence)
    
    for t in self.terms:
      self.parts.append(Atomic(t))
    
    self.known = True
    for i in self.parts:
      if hasUnknown(i.args): self.known = False

    self.implication = self.sentence.find("=>") is not -1
    self.atomic = len(self.terms) is 1

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
    for i in xrange(len(self.terms)):
      for s in subs:
        self.terms[i] = replaceArgument(self.terms[i], s[0], s[1])
    self.updateSentence()

  def subUnknown(self, subs):
    for i in xrange(len(self.terms)):
      for s in subs:
        if len(s[0]) == 1:
          self.terms[i] = replaceArgument(self.terms[i], s[0], s[1])
          
    self.updateSentence()

  def __str__(self):
    return self.sentence
    # print sentence
    # print arguments
    # p
