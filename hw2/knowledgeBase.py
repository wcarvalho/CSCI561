import re
from atomic import *
import sys

def unknown(x):
  if len(x) == 1: return True
  else: return False

def getUnknownSubs(args1, args2):
  args = len(args1)
  subs = []
  for i in xrange(args):
    if unknown(args1[i]) and not unknown(args2[i]):
      subs = subs + [(args1[i], args2[i])]
  # positions1 = unknownPos(args1)
  # positions2 = unknownPos(args2)
  # if (positions1 == positions2): return []
  # if len(positions1) > 0 and len(positions2) > 0:
  #   return makeSubs(args1, args2, positions1)
  # else:
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
  subs = [('x', '_'), ('y', '_'), ('z', '_')]
  sentence.applySubs(subs)
  return str(sentence)

def incongruent(subs):
  if (len(subs) == 0): return False
  for s in subs:
    if (not unknown(s[0]) and not unknown(s[1])):
      if s[0] != s[1]: return True
  return False

def metaSub(subs1, subs2):
  subs = subs2
  for i in xrange(len(subs1)):
    s1 = subs1[i]
    for j in xrange(len(subs2)):
      s2 = subs[j]
      if (s1[0] == s2[0]): subs[j] = (s1[1], s2[1])
  return subs

class KnowledgeBase(object):
  def __init__(self):
    self.knowledge = dict()

  def add(self, toAdd):
    if type(toAdd) is list:
      for i in toAdd:
        self.add(i)
    else:
      self.store(toAdd)

  def store(self, term):
    sentence = Sentence(term)
    if sentence.implication or sentence.atomic:
      key, value = sentence.keyValue()
      # print(key, value)
      if key in self.knowledge:
        self.knowledge[key] = self.knowledge[key] + [value]
      else: 
        self.knowledge[key] = [value]

    else:
      for t in sentence.terms:
        self.store(t)
  
  def check(self, key, arguments):
    tuples = self.knowledge[key]

    for possible in tuples:
      if possible == arguments: return True

    return False

  def search(self, key, arguments):
    tuples = self.knowledge[key]
    # print('')
    # print(len(tuples), tuples)
    # print('Search: ' + key + " -> " + str(arguments))

    subs = []
    i = 0
    for possible in tuples:
      implication = type(possible) is tuple
      # print str(i) + ": possibility: " + str(possible)

      if implication:
        antecedent = possible[0]
        variables = possible[1]

        if (i > 0): 
          fi = Sentence(recreateImplication(key, arguments, antecedent))
          consequent = fi.getConsequent()
          print "Ask: " + format(consequent)
        
        initialSubs =  makeSubs(variables, arguments)

        ant = Sentence(antecedent)
        ant.subUnknown(initialSubs)

        unknownSubs = getUnknownSubs(arguments, variables)
        subs = [] + unknownSubs

        original = str(ant)
        # print("unknown subs: " + str(unknownSubs))
        for i in xrange(len(ant.terms)):
          atom = Atomic(ant.terms[i])
          interSubs = self.ask(ant.terms[i])
          ant.applySubs(interSubs)
          # print("\t" + str(i) + ": " + str(interSubs))
          if atom.known and incongruent(interSubs): 
            print('incongruent')
            break
          subs = subs + interSubs
          

        if (original == str(ant)):
          return subs

        if (ant.known and not incongruent(subs)):
          print('returning')
          return subs

      # Predicate
      else:
        # print( possible)
        if possible == None:
          subs = makeSubs(arguments, ["x"]*len(arguments))

        elif possible == arguments:
          subs = makeSubs(possible, arguments)
        
        else:
          positions = unknownPos(arguments)
          if len(positions) > 0:
            subs = makeSubs(arguments, possible, positions)
          else:
            # print 'none'
            subs = []
            subs = makeSubs(arguments, possible)
        
      i = i + 1
        # print(subs)

    return subs

  def ask(self, query):

    sentence = Sentence(query)
    terms = sentence.terms
    atomic = len(terms) is 1

    formatted = format(str(sentence))
    print "Ask: " + formatted
    
    # if (sentence.known):
      # print 'checking'
    # else:
      # print('searching')

    if atomic:
      atom = Atomic(terms[0])

      if (sentence.known):
        if self.check(atom.pred, atom.args):
          print "True: " + formatted
          return makeSubs(atom.args, atom.args)
        else:
          substitutions = self.search(atom.pred, atom.args)
          newSentence = Sentence(atom.sentence)
          newSentence.applySubs(substitutions)
          # print('substitutions1: ' + str(substitutions))
          if (str(newSentence) == atom.sentence):
            print ("True: " + format(str(atom.sentence)))
            return substitutions
          else: 
            print ("False: " + format(str(atom.sentence)))
            return substitutions
      else:
        substitutions = self.search(atom.pred, atom.args)
        newSentence = Sentence(atom.sentence)
        newSentence.applySubs(substitutions)
        print('substitutions2: ' + str(substitutions))
        print ("True: " + format(str(newSentence)))
        # self.add(str(newSentence))
        return substitutions



    else:
      print("Haven't completed for multiple terms!")
      sys.exit(0)
