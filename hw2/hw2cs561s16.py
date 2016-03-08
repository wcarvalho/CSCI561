import argparse
import sys
from knowledgeBase import *
from atomic import *
parser = argparse.ArgumentParser(description='CSCI 561 HW2')
parser.add_argument('-i', '--input', type=file, help='input file')
parser.add_argument("-v", '--verbosity', type=int, default=1)
args = parser.parse_args()

input = args.input
if (input == None): sys.exit(0)

verbosity = args.verbosity
data = input.read().splitlines()

query = data[0]
nClauses = int(data[1])
clauses = data[2:2+nClauses]

kb = KnowledgeBase()

kb.add(clauses)

kb.ask(query)
# subs = kb.ask(query)

# q = Sentence(query)
# original = Sentence(query)

# q.applySubs(subs)
# # print(q.sentence + " vs. " + original.sentence)
# if q.known and q.sentence == original.sentence:
#   print True
# else:
#   print False

# kb.add()

# test = clauses[1]

# s = Sentence(test)
# print(s.sentence, map(s.atomic)
# y = [1,2, 10]
# map(lambda x: print(x), y)
# test

# kb.parse(clauses[0])
