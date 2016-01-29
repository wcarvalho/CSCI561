import argparse


parser = argparse.ArgumentParser(description='CSCI 561 HW1')
parser.add_argument('input', metavar='-i', type=file, help='input file')
parser.add_argument('output', metavar='-o', type=file, help='output file')
# parser.add_argument("echo")
args = parser.parse_args()
# print args.input


# args = parser.parse_args()
# input = args.input
# print (input)
lines = tuple(open(input, 'r'))