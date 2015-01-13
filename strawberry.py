#!/usr/bin/env python

import sys 
import os 
import argparse

f_path = os.path.dirname(__file__)
sys.path += [".", 
             f_path, 
             "%s/util" % f_path, 
             "%s/xcode" % f_path]

from colors import Colors

try:
  from strawberry_config import Config 
except ImportError:
  sys.stdout.write("%sError%s: Unable to find strawberry_config.py, would you like to run setup? Y/N: " %(Colors.RED, Colors.NORMAL))
  ans = raw_input()
  if ans == "y" or ans == "Y":
    from setup import setup
    setup()
    exit(0)
  else:
    exit(1)

from command import run_cmd 
from target import Target, sdks
from build import build
from xc_test import test  
from setup import setup

def print_targets():
  print("Available targets:\n")
  for t in Config.targets:
    print("\t%s" % t.name)
  print("")

def print_sdks():
  print("Available sdks:\n")
  for s in sdks:
    print("\t%s" % s)
  print("")

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('-c', '--clean', action='store_true', help='Clean befroe build')
  parser.add_argument('-t', '--target', help='The target')
  parser.add_argument('--list-targets', action='store_true', help='Prints the available targets')
  parser.add_argument('-s', '--sdk', default=sdks[0], help='The SDK')
  parser.add_argument('--list-sdks', action='store_true', help='Lists the available SDKs')
  parser.add_argument('-r', '--run', action='store_true', help='Run after build')
  parser.add_argument('-b', '--build', action='store_true', help='Build')
  parser.add_argument('--test', action='store_true', help='Run tests')
  parser.add_argument('-v', '--verbose', action='store_true', help='Prints output for all commands')
  parser.add_argument('-d', '--debug', action='store_true', help='Print debug information')
  args = parser.parse_args()
  debug = args.debug
  if debug:
    print('Args: ' + str(args))

  if args.list_targets:
    print_targets()
    exit(0)
  elif args.list_sdks:
    print_sdks()
    exit(0)

  if args.target == None:
    print("You need to provide a target, try --list-targets to see which are available or --help to see the help")
    exit(1)

  target_li = [t for t in Config.targets if t.name == args.target]
  if len(target_li) != 1:
    print("Invalid target: %s" % args.target)
    exit(1)

  sdk_li = [s for s in sdks if s == args.sdk]
  if len(sdk_li) != 1:
    print("Invalid sdk: %s" % sdk_in)
    exit(1)

  if args.build:
    build(args.clean, target_li[0], sdk_li[0], args.run, args.verbose)

  if args.test:
    test(target_li[0], sdk_li[0], verbose=args.verbose)

if __name__ == '__main__': 
  main()

