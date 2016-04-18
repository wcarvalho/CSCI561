import argparse
import sys
from io import *
from network import *
from calculator import *

parser = argparse.ArgumentParser(description='CSCI 561 HW2')
parser.add_argument('-i', '--input', type=file, help='input file')
parser.add_argument("-v", '--verbosity', type=int, default=0)
args = parser.parse_args()

input = args.input
if (input == None): sys.exit(0)

verbosity = args.verbosity

data = input.read().splitlines()

queries, networkStart = getQueries(data)

nodeInfo = seperateNodeInfo(data[networkStart:])


net = Network(nodeInfo, verbosity)
if verbosity > 1: net.pp()

calculator = Calculator(net, verbosity)

answers = []
for q in queries:
  a = calculator.calculate(q)
  if verbosity > 0: print "answer:", a
  Q = Query(q)
  if (Q.type == "P"):
    answer = str(
      format(roundFloat(a), '.2f')
      )
  elif (Q.type == "EU"): 
    answer = str(roundInt(a))
  elif (Q.type == "MEU"): 
    answer = arrayToString(a[0]) + " " + str(roundInt(a[1]))

  answers.append(answer)

with open("output.txt", "w") as text_file:
    text_file.write(arrayToIOString(answers))