from node import *
from query import *

class Network(object):
  def __init__(self, nodeInfo, verbosity=0):
    self.v = verbosity
    self.nodes = {}
    self.addNodes(nodeInfo)

  def contains(self, args):
    args = sorted(args)
    for i in self.nodes:
      node = self.nodes[i]
      nodeargs = node.argumentMap.keys()
      nodeargs = sorted(nodeargs)
      if nodeargs == args: return True
      else: return False
  
  def parentsOf(self, name):
    return self.nodes[name].parents.keys()
  def getValue(self, query, level):
    qargs = query.args
    for i in self.nodes:
      node = self.nodes[i]
      nargs = node.ordered_args
      if self.v > 1: print "\t"*level + "node_args", nargs
      if self.v > 1: print "\t"*level + "q_args", qargs
      
      if nargs == qargs: 
        if self.v > 1: print "\t"*(level+1) + "MATCH"
        return node.getValue(query.arguments)
       
    return None

  def findDependencies(self, args):
    # print "args: " + str(args)
    table = {}
    for a in args:
      table[a]=self.nodes[a].parents.keys()

    # print table
    return {}
    # for a in args:
    #   node = self.nodes[a]
    #   parents = node.parents.keys()
    #   print "\tname: " + str(node.name)
    #   print "\tparents: " + str(parents)
    #   common = set(args).intersection(set(parents))
    #   print "\tcommon: " + str(common)
    #   if len(common) > 0: return False
    return True

  def getAncestors(self, name):
    node = self.nodes[name]
    ancestors = node.parents.keys()
    for i in ancestors:
      ancestors = ancestors + self.getAncestors(i)
    return ancestors
  
  def getDecisionNodes(self):
    nodes = []
    for i in self.nodes:
      node = self.nodes[i]
      if node.type == "decision": 
        nodes.append(node.name)
    return nodes
  
  def getUtilityArguments(self):
    for i in self.nodes:
      node = self.nodes[i]
      if node.type == "utility":
        args = set(node.argumentMap.keys()) - set(['utility'])
        return list(args)

  def getAncestorChain(self, name, assignments):
    parents = self.parentsOf(name)
    if len(parents) == 0:
      if self.nodes[name].type == "decision": return []
      return [constructJoint([name], assignments)]
    functions = []
    f = constructConditional(assignments, [name], parents)
    functions.append(f)
    for i in parents:
      functions = functions + self.getAncestorChain(i, assignments)
    return functions
  def addNodes(self, nodeInfo):
    for info in nodeInfo:
      name, parents = seperateNameParents(info[0])
      node = Node(name, info, self.v)
      self.nodes[name] = node

      for p in parents:
        parent = self.nodes[p]
        node.addParent(parent)
        parent.addChild(node)

  def pp(self):
    for i in self.nodes:
      self.nodes[i].pp()
    # for i in nodes:
    #   self.nodes.add(i)
