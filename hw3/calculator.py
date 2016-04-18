from network import *
from query import *
from node import *
import itertools

# def nCr(n,r):
#   f = math.factorial
#   return f(n) / f(r) / f(n-r)

def getAllCombinations(unknowns):

  table = list(itertools.product([True, False], repeat=len(unknowns)))

  combinations = []

  for i in table:
    combo = {}
    for j in xrange(len(unknowns)):
      combo[unknowns[j]] = i[j]
    combinations.append(combo)

  return combinations

def getQueriesAndUnknowns(chain):
  terms = set(chain)
  queries = []
  unknowns = []
  for t in terms:
    qp = Query(t)
    queries.append(qp)
    unknowns = unknowns + qp.getUnknowns()

  unknowns = list(set(unknowns))
  return queries, unknowns
      
class Calculator(object):
  def __init__(self, network, verbosity=0):
    self.network = network
    self.v = verbosity
    self.l = 0
    self.assignments = {}

  def calculate(self, query):

    q = Query(query)
    self.assignments.update(q.arguments)
    if (q.type == "P"): 
      return self.probability(query)
    elif (q.type == "EU"): 
      return self.utility(query)
    elif (q.type == "MEU"): 
      return self.maxUtility(query)

  def readQuery(self, query):
    q = Query(query)
    self.pp('-----------', 0)
    self.pp(query, 0)

    fargs = q.arguments
    args = q.args
    return q, fargs, args

  def getMarginalParents(self, args):
    parents = set()
    for a in args:
      pars = self.network.nodes[a].parents.keys()
      for p in pars:
        parents.add(p)
      # add each parent
      map(parents.add, (set(pars)))
      # set's compliment to only keep parents not in arguments
      parents = parents - set(args)
    options = {}
    for p in parents:
      options [p] = [True, False]
    return parents
  
  def pp(self, str, min_verbosity):
    if self.v > min_verbosity:
      print "\t"*(self.l-1) + str
  # returns all members of post that are ancestors of members in pre
  def getPostAncestors(self, pre, post):
    ancestors = set()
    real = set()
    print post
    for o in post:
      map(ancestors.add, self.network.getAncestors(o))

    self.pp("\tall ancestors: " + str(ancestors), 1)
    for r in pre:
      if r in ancestors: real.add(r)
    return list(real)

  def returnVal(self, query, value, verbosity):
    self.pp(query + " = " + str(value), verbosity)
    self.l = self.l - 1 
    return value

  def probability(self, query):
    self.l = self.l + 1
    q, fargs, args = self.readQuery(query)

    value = self.network.getValue(q, self.l)
    if value != None:
      return self.returnVal(query, value, 0)

    if q.conditional():
      val = self.conditional(q, args, fargs)
    else:
      val = self.joint(args, fargs)
    
    return self.returnVal(query, val, 0)
  
  def conditional(self, q, args, fargs):
    self.pp("CONDITIONAL", 0)
    
    pre, post = q.getPrePost()
    self.pp("\tpre, post: " + str(pre) + ", " + str(post), 1)
    
    # post_ancestors = self.getPostAncestors(pre, post)
    # self.pp("\t" + str(post_ancestors) + " ancestors of " + str(post), 0)
    
    # if len(post_ancestors) > 0:
    top, bottom = bayesRule(pre, post, fargs)
    # print query + "=\n\t" + top1 + "*" + top2+"/" + bottom
    self.pp("\t"+q.str + " = ", 0)
    self.pp("\t\t" + top +"/" + bottom, 0)

    val = self.probability(top)/self.probability(bottom)
    return val

  def joint(self, args, fargs):
    pass
    self.pp("JOINT", 0)

    chain = []
    for i in args:
      chain = chain + self.network.getAncestorChain(i, fargs)

    queries, unknowns = getQueriesAndUnknowns(chain)
    combinations = getAllCombinations(unknowns)

    self.pp("\tchain:" + str (set(chain)), 1)
    self.pp("\tunknowns:" + str (unknowns), 0)
    self.pp("\tcombinations:" + str (combinations), 1)

    sum = 0
    for i in combinations:
      prob = 1.
      for qp in queries: 
        qp.setArguments(i)
        pr = self.probability(qp.str)
        prob = prob * pr
      self.pp(str(i),0)
      self.pp(str(chain)+ "=" + str(prob),0)
      sum = sum + prob
    return sum

  def utility(self, query):
    self.l = self.l + 1
    q, fargs, args = self.readQuery(query)

    uargs = self.network.getUtilityArguments()      # parents of utility node
    dnodes = self.network.getDecisionNodes()
    if q.conditional():
      pre1, post = q.getPrePost()
      pre2 = list(set(uargs) - set(dnodes))
      query = constructConditional(fargs, pre2, post + pre1)
    else:
      query = constructJoint(uargs + args, fargs)

    queries, unknowns = getQueriesAndUnknowns([query])
    combinations = getAllCombinations(unknowns)
    q2 = queries[0]

    utilityQuery = constructUtilityQuery(uargs, fargs)
    uq = Query(utilityQuery)

    sum = 0
    for i in combinations:
      q2.setArguments(i)
      uq.setArguments(i)
      self.pp(q2.str + "*" + uq.str, 0)
      p = self.probability(q2.str)
      self.pp("\t\tP = " + str(p),0)
      v = self.network.getValue(uq, self.l)
      self.pp("\t\tU = " + str(v),0)
      sum = sum + p*v
      self.pp(q2.str + "*" + uq.str + " = " + str(p*v), 0)

    return sum
    self.l = self.l - 1

  def maxUtility(self, query):
    self.l = self.l + 1
    queries, unknowns = getQueriesAndUnknowns([query])
    combinations = getAllCombinations(unknowns)
    
    utilityQuery = query.replace("MEU", "EU")
    q, fargs, args = self.readQuery(utilityQuery)

    eu = []
    for i in combinations:
      q.setArguments(i)
      eu.append(self.utility(q.str))

    best = (-1e10, [])
    for i in xrange(len(eu)):
      u = eu[i]
      combo = combinations[i]
      formatted_combo = argmapToList(q.args, combo)
      self.pp(str(formatted_combo) + ": " + str(u), 0)
      if u > best[0]:
        best = (u, formatted_combo)

    return best[1], best[0]
    self.l = self.l - 1

