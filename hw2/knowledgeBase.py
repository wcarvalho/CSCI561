import re
from atomic import *

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

def format(query):
  sentence = Sentence(query)
  subs = [('x', '_'), ('y', '_'), ('z', '_')]
  sentence.applySubs(subs)
  return str(sentence)

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
      self.knowledge[key] = [value]
    else:
      for t in sentence.terms:
        self.store(t)

  def ask(self, query):
    sentence = Sentence(query)
    terms = sentence.terms
    
    print "Ask: " + format(query)
    
    true = True
    # for when there is more than one term
    if (len(terms) > 1 ):
      for t in terms:
        true = true and self.ask(t)
      return true

    # otherwise
    a = Atomic(terms[0])
    subs = self.search(a.pred, a.args)
    sentence = Sentence(a.sentence)
    sentence.applySubs(subs)
    
    formatted = format(str(sentence))
    
    newA = Atomic(sentence.terms[0])
    if newA.known:
      if self.check(newA.pred, newA.args) or formatted == query:
        print "True: " + formatted
        # return makeSubs(newA.args, newA.args)
      # elif formatted == query:
      else: 
        print "False: " + formatted
    else: 
      print "False: " + formatted
    
    return subs
    
      # else:
      # print "True: " + formatted
      #   print "False: " + query
      #   return makeSubs(a.args, len(a.args)*["x"])
      
    # print(subs)


  def search(self, key, arguments):

    # print('search: ' + key + " -> " + str(arguments))
    tuples = self.knowledge[key]

    i = 0
    for possible in tuples:
      implication = type(possible) is tuple
      # print("implication: " + str(implication))
      # print(possible)
      if implication:
        antecedent = possible[0]
        variables = possible[1]
        sentence = Sentence(antecedent)
      
        subs = []
        for t in sentence.terms:
          subs = subs + self.ask(t)
        
        fullImplication = recreateImplication(key, variables, antecedent)
        sentence = Sentence(fullImplication)
        sentence.applySubs(subs)
        
        consequent = Sentence(sentence.getConsequent())
        consArgs = consequent.parts[0].args
        return makeSubs(arguments, consArgs)

      else:
        if possible == None:
          return makeSubs(arguments, ["x"]*len(arguments))
          # return makeSubs(arguments, arguments)
        else:
          # print possible
          # print arguments
          positions = unknownPos(arguments)
          # print positions
          if len(positions) > 0:
            return makeSubs(arguments, possible, positions)
          else:
            return makeSubs(arguments, arguments)
            # if (self.check(key, arguments)):
            # else:
              # return makeSubs(arguments, ["x"]*len(arguments))

        # original_arguments = arguments
          # arguments[pos] = possible[pos]
        # if possible == arguments: 
          # subs=[]
          # for pos in positions:
      i = i + 1

    return False

  def check(self, key, arguments):
    tuples = self.knowledge[key]

    for possible in tuples:
      if possible == arguments: return True

    return False
