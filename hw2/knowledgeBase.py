import re
from atomic import *
import sys

KEYS = '123456789abcdefghijklmnopqrstuvwxyz'

def unknown(x):
  if len(x) == 1: return True
  else: return False

def getUnknownSubs(args1, args2):
  args = len(args1)
  subs = []
  for i in xrange(args):
    if unknown(args1[i]) and not unknown(args2[i]):
      subs = subs + [(args1[i], args2[i])]

  return subs

def makeSubs(arguments, possible, positions=None):
  subs=[]
  if (positions == None):
    for pos in xrange(len(arguments)):
      subs.append((arguments[pos], possible[pos]))
  else:
    for pos in positions:
      subs.append((arguments[pos], possible[pos]))
  return subs

def recreateImplication(key, variables, antecedent):

  sentence = antecedent + "=>"+ key + "("
  for i in xrange(len(variables)-1):
    v = variables[i]
    sentence = sentence + v + ","
  sentence = sentence + variables[len(variables)-1] + ")"
  return sentence

def substitute(sentence, vars, args):
  s = Sentence(sentence)
  subs = makeSubs(vars, args)
  s.applySubs(subs)
  return str(s)
def format(query):
  sentence = Sentence(query)
  sentence.cleanUnknown()
  return str(sentence.sentence.replace(",", ", ").replace("&&", " && "))

def incongruent(subs):
  if (len(subs) == 0): return False
  for s in subs:
    if (not unknown(s[0]) and not unknown(s[1])):
      # print "incongruent: " + s[0] + " vs. " + s[1]
      if s[0] != s[1]: return True
  return False

class KnowledgeBase(object):
  def __init__(self, verbosity):
    self.knowledge = dict()
    self.false = dict()
    self.v = verbosity
    self.link = []
    self.level = -1
    self.usedVariables = set()
    self.varkey = 0
    self.explored = set()

  def tab(self):
    return "\t"*self.level

  def tabUp(self):
    return "\t"*(self.level+1)

  def vprint(self, lev, str):
    if (self.v > lev): print str

  def exploredKey(self, parent, term, child, argument):
    return str(parent)+str(term) + "," + str(child) + "," + str(argument)

  def wasExplored(self, parent, term, child, argument):
    ekey = self.exploredKey(parent, term, child, argument) 
    true = ekey in self.explored
    self.vprint(2, self.tab()+'was explored: ' + ekey + ", " + str(true))
    return ekey in self.explored

  def addExplored(self, parent, term, child, argument):
    key = self.exploredKey(parent, term, child, argument)
    self.vprint(2, self.tab() + 'adding explored: ' + key)
    self.explored.add(key)

  def addFalse(self, add):
    self.storeChain("False: " + format(add))
    sentence = Sentence(add)
    for p in sentence.parts:
      key = p.pred
      value = p.args
      if key in self.false:
        self.false[key] = self.false[key] + [value]
      else: 
        self.false[key] = [value]

  def replicate(self):
    self.copy = self.knowledge.copy()
    return self.copy

  def add(self, toAdd):
    if type(toAdd) is list:
      for i in toAdd:
        self.add(i)
    else:
      self.store(toAdd)

  def addNew(self, toAdd):
    if (self.v > 1):
      print(self.tab() + "---Adding: " + str(toAdd))
    atom = Atomic(toAdd)
    if not self.check(atom.pred, atom.args):
      self.add(toAdd)


  def show(self):
    print self.tab()+'------------- KNOWLEDGE -------------'
    for i in self.knowledge:
      print self.tab()+ str(i) + ", " + str(self.knowledge[i])
    print self.tab()+'------------- --------- -------------'
  
  def store(self, term):
    sentence = Sentence(term)
    variables = sentence.getVariables()
    for v in variables:
      if (unknown(v)):
        sub = [(v, KEYS[self.varkey])]
        self.varkey = self.varkey + 1
        sentence.applySubs(sub)
    
    if sentence.implication or sentence.atomic:
      key, value = sentence.keyValue()
      if key in self.knowledge:
        self.knowledge[key] = self.knowledge[key] + [value]
      else: 
        self.knowledge[key] = [value]

    else:
      for t in sentence.terms:
        self.store(t)
  
  def storeChain(self, link):
    if (self.v > 0): 
      print self.tab() + link
    self.link.append(link)

  def getChain(self):
    str = ""
    for i in self.link:
      str = str + i + "\r\n"

    return str

  def check(self, key, arguments):
    tuples = self.knowledge[key]

    for possible in tuples:
      if (self.v > 3): 
        print str(possible) + " vs. " + str(arguments)
      if possible == arguments: return True

    return False

  def availableOptions(self, parent, key, level):
    # print('getting availableOptions for ' + key)
    original_level = self.level
    self.level = level
    atom = Atomic(key)
    options = self.copy[atom.pred]
    available = []

    i = 0
    for opt in options:
      implication = type(opt) is tuple
      if implication:
        antecedent = opt[0]
        s = Sentence(antecedent)
        for t in s.terms:
          available.append(self.availableOptions(atom.pred,t, level + 1))
      else:
        explored = self.wasExplored(parent, i, atom.pred, opt)
        if not (explored):
          available.append(opt)
      i = i + 1
    print(available)
    # sys.exit(0)
    self.level = original_level
    return available

  def implicationContingency(self, parent, subs, newSubAlpha, antecedent, j):
    checkNext = False
    self.vprint(0, self.tab()+'NOT IN KB: ' + antecedent.sentence)
    
    reversedSubs = lastReversedSub(subs)
    if (len(reversedSubs) == 0):
      checkNext = True
      return checkNext, subs
    else:

      self.vprint(0, self.tab()+"reversed sub:" + str(reversedSubs))
      
      antecedent.applySubs(reversedSubs)
      self.vprint(0, self.tab() + "reversed sentence: " + antecedent.sentence)
      
      previousKey = antecedent.terms[j-1]
      # opts = self.availableOptions(parent,previousKey, self.level + 1)
      # self.vprint(0, self.tab() + "number of available options: " + str(len(opts)))
      

      lastAtom = Atomic(previousKey)

      abl = allButLastSub(subs)
      
      newSubs = self.search(lastAtom.pred, j-1, lastAtom.pred, lastAtom.args, abl)
      # if (incongruent(newSubs)):
      #   checkNext = True
      #   return checkNext, abl+newSubs
      self.vprint(0, self.tab() + "new sub: " + str(newSubs))
      antecedent.applySubs(newSubs)
      self.addTrue(parent, j-1, Atomic(antecedent.terms[j-1]))

      return checkNext, abl+newSubs
      # availOpts = self.availableOptions(parent, previousKey)
      # self.vprint(0, self.tab()+"available options: " + str(availOpts))

  def searchImplication(self, parent, key, arguments, givenSubs, i, possible):
    antecedent = possible[0]
    variables = possible[1]

    if (i > 0): 
      fi = Sentence(recreateImplication(key, arguments, antecedent))
      consequent = fi.getConsequent()
      self.storeChain("Ask: " + format(consequent))
    

    initialSubs = givenSubs+ makeSubs(variables, arguments)
    ant = Sentence(antecedent)
    ant.subUnknown(initialSubs)
    self.vprint(0,self.tab() + "starting sentence: " + ant.sentence)

    subs = getUnknownSubs(arguments, variables)

    original = str(ant)
    checkNext = False
    j = 0
    while j < len(ant.terms):
      t = ant.terms[j]
      interSubs = self.ask(ant.terms[j], key, j)
      if not incongruent(interSubs):
        ant.applySubs(interSubs)
      atom = Atomic(ant.terms[j])
      original_post = ant.sentence
      # self.addExplored(key, atom.pred, atom.args)
      self.vprint(0, self.tab() + str(j) +": " + t + " -> " + ant.terms[j])
      self.vprint(0, self.tab()+"subs so far: " + str(subs+interSubs))
      self.vprint(0, self.tab() + "sentence post: " + original_post)

      if (self.v > 3): self.show()
      if (not self.check(atom.pred, atom.args)):

          if not incongruent(subs):
            checkNext, subs = self.implicationContingency(parent, subs, interSubs, ant, j)

          # else: checkNext = True

          if (checkNext): break
          if (len(subs) > 0):
            j = j - 1
      j = j + 1

      if not incongruent(interSubs):
        subs = subs + interSubs
    
    # print ("BROKE AND RETURNING:", (subs, original, ant.sentence, checkNext))
    return subs, original, ant, checkNext



  def search(self, parent, term, key, arguments, givenSubs = []):
    tuples = self.knowledge[key]
    self.vprint(0, self.tab()+'Search: ' + key + " -> " + str(arguments))
    # self.vprint(0, self.tab()+ str(len(tuples)) + " options: " +str(tuples))

    subs = []
    i = 0
    for possible in tuples:
      implication = type(possible) is tuple
      self.vprint(0, self.tab()+"-O-" + str(i) + ": " + str(possible))
      # print str(i) + ": possibility: " + str(possible)

      if implication:
        subs, original_antecedent, new_antecedent, checkNext = self.searchImplication(parent, key, arguments, givenSubs, i, possible)
        if (original_antecedent == str(new_antecedent) and len(subs) > 0) or not checkNext:
          # print 'returning ' + str(subs)
          return subs

      else:
        if possible == None:
          subs = makeSubs(arguments, ["x"]*len(arguments))

        elif possible == arguments:
          subs = makeSubs(possible, arguments)
        
        else:
          upositions = unknownPos(arguments)
          kpositions = knownPos(arguments)
          if len(upositions) > 0:
            match = sameKnown(arguments, possible, kpositions)
            explored = self.wasExplored(parent, term, key, possible)
            if (match and not explored):
                return makeSubs(arguments, possible, upositions)

          else:
            subs = makeSubs(arguments, possible)
        
      i = i + 1

    return subs

  def indexOfOpt(self, key, args):
    opts = self.copy[key]
    for i in xrange(len(opts)):
      opt = opts[i]
      if opt == args: return i
    return -1

  def ask(self, query, parent = '', term=0):
    self.level = self.level + 1
    sentence = Sentence(query)
    terms = sentence.terms
    atomic = len(terms) is 1

    formatted = format(str(sentence))
    
    if atomic:
      atom = Atomic(terms[0])
      
      ### TEMPORARY HACK -- LOOK FOR BETTER!!!
      if (self.wasExplored(parent, term, atom.pred, atom.args)):
        self.level = self.level - 1
        return []
      ###################

      self.storeChain("Ask: " + formatted)
      if (sentence.known):
        if self.check(atom.pred, atom.args):
            # pass
          self.storeChain("True: " + formatted)
          self.level = self.level - 1
          return []
        else:
          newSentence, newAtom, substitutions = self.getSearchResults(parent, term, atom)
          if (str(newSentence) == atom.sentence):
            resultTerm = self.indexOfOpt(newAtom.pred, newAtom.args)
            self.addTrue(parent, term, newAtom)
            self.level = self.level - 1
            return substitutions
          else:
            self.addFalse(format(str(atom.sentence)))
            self.level = self.level - 1
            # return []
            return substitutions
      else:
        newSentence, newAtom, substitutions = self.getSearchResults(parent, term, atom)
        if newSentence.known: 
          resultTerm = self.indexOfOpt(newAtom.pred, newAtom.args)
          self.addTrue(parent, term, newAtom)
        else: substitutions = []
        
        self.level = self.level - 1
        return substitutions

    else:
      substitutions = []
      i = 0
      for t in terms:
        substitutions = substitutions + self.ask(t, parent, i)
        i = i +1

      self.level = self.level - 1
      return substitutions

  def getSearchResults(self, parent, term, atom):
    substitutions = self.search(parent, term, atom.pred, atom.args)
    if incongruent(substitutions): substitutions = makeSubs(atom.args, ["x"]*len(atom.args))
    newSentence = Sentence(atom.sentence)
    newSentence.applySubs(substitutions)
    newAtom = Atomic(newSentence.terms[0])
    return newSentence, newAtom, substitutions

  def addTrue(self, parent, term, atom):
    self.storeChain("True: " + format(str(atom.sentence)))
    self.addNew(str(atom.sentence))
    self.addExplored(parent, term, atom.pred, atom.args)
    