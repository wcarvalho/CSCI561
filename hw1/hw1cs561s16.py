import argparse
import sys
from ai import *


parser = argparse.ArgumentParser(description='CSCI 561 HW1')
parser.add_argument('-i', '--input', type=file, help='input file')
# parser.add_argument("-a", '--algorithm', type=int, help='algorithm', default=1)
parser.add_argument("-v", '--verbosity', type=int, default=1)
args = parser.parse_args()

input = args.input

if (input == None): sys.exit(0)

verbosity = args.verbosity

data = input.read().splitlines()
ai = AI(data, verbosity)

task = int(data[0])

def writeNext(next):
  with open("next_state.txt", "w") as text_file:
    text_file.write(next)


def writeTraversal(traversal):
  with open("traverse_log.txt", "w") as text_file:
    text_file.write(traversal)

if (task == 1): 
  path = ai.task1()
  next = getNextFromPath(path)
  writeNext(getBoardFromState(ai, next))
  
elif (task == 2): 
  next, traversalString = ai.task2()
  writeNext(getBoardFromState(ai, next))
  writeTraversal(traversalString)
  
elif (task == 3): 
  next, traversalString = ai.task3()
  writeNext(getBoardFromState(ai, next))
  writeTraversal(traversalString)
  
elif (task == 4):
  traversalString = ai.task4()
  with open("trace_state.txt", "w") as text_file:
    text_file.write(traversalString)

