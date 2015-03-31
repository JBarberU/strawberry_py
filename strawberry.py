#!/usr/bin/env python

import sys
import os
import argparse

f_path = os.path.dirname(__file__)
sys.path += [".",
             f_path,
             "%s/lib" % f_path,
             "%s/util" % f_path,
             "%s/xcode" % f_path,
             "%s/formatters" % f_path]

from colors import Colors

from xc_config import Config
from xc_target import Target, sdks
from xc_build import XCodeBuildBase
from xc_test import test
from xc_test import TestFocusObject
from xc_test import TestExcludeObject
from setup import setup
from log import Log
from xc_utils import get_device
from build_xml_formatter import BuildXMLFormatter

def print_targets(config):
  print("Available targets:\n")
  for t in config.targets:
    print("\t%s" % t.name)
  print("")

def print_sdks():
  print("Available sdks:\n")
  for s in sdks:
    print("\t%s" % s)
  print("")

def main():

  config = Config("straw_conf.json")

  parser = argparse.ArgumentParser()
  parser.add_argument("-c", "--clean", action="store_true", help="Clean befroe build")
  parser.add_argument("-t", "--targets", nargs="+", help="The target")
  parser.add_argument("--list-targets", action="store_true", help="Prints the available targets")
  parser.add_argument("-s", "--sdk", help="The SDK")
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
    config.clean = True
  if args.targets:
    config.targets = args.targets
  if args.sdk:
    config.sdk = args.sdk
  if args.run:
    config.run = True
  if args.build:
    config.build = True
  if args.test:
    config.test = True
  if args.focus:
    config.focus = args.focus
  if args.exclude:
    config.exclude = args.exclude
  if args.retry_count:
    config.retry_count = args.retry_count
  if args.reinstall:
    config.reinstall = True
  if args.verbose:
    config.verbose = True
  if args.debug:
    config.debug = True

  if config.debug:
    Log.info("Args: " + str(args))

  if args.list_targets:
    print_targets(config)
    exit(0)
  elif args.list_sdks:
    print_sdks()
    exit(0)

  if not config.targets:
    Log.fatal("You need to provide at least none target, try --list-targets to see which are available or --help to see the help")
  else:
    t_li = [x for x in config.available_targets if x.name in config.targets]
    if len(t_li) == 0:
      Log.fatal("You can't use a non-unique target name")
    config.sel_targets = t_li

  sdk_li = [s for s in sdks if s == config.sdk]
  if len(sdk_li) != 1:
    Log.fatal("Invalid sdk \"{0}\"".format(sdk_in))

  if not config.build_dir:
    Log.fatal("Build dir not set")
  else:
    build_dir = "{0}/{1}".format(os.getcwd(), config.build_dir)
    if os.path.exists(os.path.dirname(build_dir)):
      config.build_dir = build_dir
    elif not os.path.exists(os.path.dirname(config.build_dir)):
      Log.fatal("Build dir doesn't exist")

  if not config.device:
    default_device = "iPhone 5s (8.1 Simulator)"
    config.device = get_device(default_device)
    Log.warn("Using the default device: \"{0}\"".format(default_device))

  if config.build:
    builder = XCodeBuildBase.create_builder(config)
    if config.build_report_format:
      if config.build_report_format == "xml":
        result_formatter = BuildXMLFormatter(config.build_report_file)
      else:
        Log.warn("Unknown build_report_format \"{0}\"".format(config.build_report_format))
        result_formatter = None
    else:
      result_formatter = None
    if not builder.build(result_formatter):
      result_formatter.save()
      Log.fatal("Failed to build! Aborting...")

    if result_formatter:
      result_formatter.save()

  if config.test:
    test(config)

  Log.msg("Done!")

if __name__ == "__main__":
  main()

