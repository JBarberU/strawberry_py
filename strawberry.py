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
    from setup import setup
    setup()
    exit(0)

from target import Target, sdks
from xc_build import XCodeBuildBase
from xc_test import test
from xc_test import TestFocusObject
from xc_test import TestExcludeObject
from setup import setup
from log import Log
from xc_utils import get_device

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
  parser.add_argument("-c", "--clean", action="store_true", help="Clean befroe build")
  parser.add_argument("-t", "--target", help="The target")
  parser.add_argument("--list-targets", action="store_true", help="Prints the available targets")
  parser.add_argument("-s", "--sdk", default=sdks[0], help="The SDK")
  parser.add_argument("--list-sdks", action="store_true", help="Lists the available SDKs")
  parser.add_argument("-r", "--run", action="store_true", help="Run after build")
  parser.add_argument("-b", "--build", action="store_true", help="Build")
  parser.add_argument("--test", action="store_true", help="Run tests")
  parser.add_argument("--focus", nargs="+", help="Only run the given tests")
  parser.add_argument("--exclude", nargs="+", help="Run all but the given tests")
  parser.add_argument("--retry-count", type=int, help="The number of times to retry a failed test")
  parser.add_argument("--reinstall", action="store_true", help="Reinstalls the app between each test")
  parser.add_argument("-v", "--verbose", action="store_true", help="Prints output for all commands")
  parser.add_argument("-d", "--debug", action="store_true", help="Print debug information")
  args = parser.parse_args()

  if args.clean:
    Config.clean = True
  if args.target:
    Config.target = args.target
  if args.sdk:
    Config.sdk = args.sdk
  if args.run:
    Config.run = True
  if args.build:
    Config.build = True
  if args.test:
    Config.test = True
  if args.focus:
    Config.focus = args.focus
  if args.exclude:
    Config.exclude = args.exclude
  if args.retry_count:
    Config.retry_count = args.retry_count
  if args.reinstall:
    Config.reinstall = True
  if args.verbose:
    Config.verbose = True
  if args.debug:
    Config.debug = True

  if Config.debug:
    Log.info("Args: " + str(args))

  if args.list_targets:
    print_targets()
    exit(0)
  elif args.list_sdks:
    print_sdks()
    exit(0)

  if Config.target == None:
    Log.fatal("You need to provide a target, try --list-targets to see which are available or --help to see the help")

  target_li = [t for t in Config.targets if t.name == Config.target]
  if len(target_li) != 1:
    Log.fatal("Invalid target \"{0}\"".format(Config.target))

  sdk_li = [s for s in sdks if s == Config.sdk]
  if len(sdk_li) != 1:
    Log.fatal("Invalid sdk \"{0}\"".format(sdk_in))

  if not Config.build_dir:
    Log.fatal("Build dir not set")
  else:
    build_dir = "{0}/{1}".format(os.getcwd(), Config.build_dir)
    if os.path.exists(os.path.dirname(build_dir)):
      Config.build_dir = build_dir
    elif not os.path.exists(os.path.dirname(Config.build_dir)):
      Log.fatal("Build dir doesn't exist")

  if not Config.device:
    default_device = "iPhone 5s (8.1 Simulator)"
    Config.device = get_device(default_device)
    Log.warn("Using the default device: \"{0}\"".format(default_device))

  if Config.build:
    builder = XCodeBuildBase.create_builder(target_li[0], sdk_li[0], Config.build_dir)
    if not builder.build(Config.clean, Config.run, Config.device, Config.verbose):
      Log.fatal("Failed to build! Aborting...")

  if Config.test:
    if Config.focus:
      focus_object = TestFocusObject(Config.focus)
    elif Config.exclude:
      focus_object = TestExcludeObject(Config.exclude)
    else:
      focus_object = None

    test(target_li[0], sdk_li[0], focus_object, Config.retry_count, Config.reinstall, verbose=Config.verbose)

  Log.msg("Done!")

if __name__ == "__main__":
  main()

