import argparse
import sys
from knowledgeBase import *
from atomic import *
parser = argparse.ArgumentParser(description='CSCI 561 HW2')
parser.add_argument('-i', '--input', type=file, help='input file')
parser.add_argument("-v", '--verbosity', type=int, default=0)
args = parser.parse_args()

input = args.input
if (input == None): sys.exit(0)

verbosity = args.verbosity
data = input.read().splitlines()

query = data[0]
nClauses = int(data[1])
clauses = data[2:2+nClauses]

kb = KnowledgeBase(verbosity)

kb.add(clauses)
kb.replicate()

if (verbosity > 0):
  kb.show()
  print("\n"*3)

# sys.exit(1)
substitutions = kb.ask(query)

q = Sentence(query)
if not q.known: q.applySubs(substitutions)

# kb.show()

true = True
for t in q.terms:
  atom = Atomic(t)
  if not kb.check(atom.pred, atom.args):
    true = False
    break

output = kb.getChain()

if true:
  output = output + "True"
else:
  output = output + "False"

inputFile = input.name
prefix = inputFile[inputFile.find("/")+1:inputFile.find(".txt")]

with open("output.txt", "w") as text_file:
    text_file.write(output)
