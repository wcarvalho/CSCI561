import argparse
from ai import *

parser = argparse.ArgumentParser(description='CSCI 561 HW1')
parser.add_argument('input', type=file, help='input file')
parser.add_argument("-a", '--algorithm', type=int, help='algorithm', default=1)
parser.add_argument("-v", '--verbosity', type=int, help='algorithm', default=1)
args = parser.parse_args()

input = args.input
verbosity = args.verbosity
algorithm = args.algorithm

data = input.read().splitlines()
ai = AI(data, algorithm, verbosity)

ai.simulate()