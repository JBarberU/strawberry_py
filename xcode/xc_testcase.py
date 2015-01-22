from number_helper import number_string_with_postfix
from xc_exception import TestFailureError
from output_pipe import OutputPipe
from command import run_cmd_ret_output
from strawberry_config import Config
from shutil import rmtree
from log import Log
from colors import Colors
import os
import random
import tempfile

class TestCase:
  result = False
  file_name = ""
  target = None
  time_spent = ""
  output = []
  run_number = 0

  def __init__(self, file_name_in, target):
    self.file_name = file_name_in
    self.target = target

  def __create_folders(self):
    if not Config.test_results_dir:
      test_results_dir = "/tmp/results"
    else:
      test_results_dir = Config.test_results_dir

    try:
      os.makedirs(test_results_dir)
    except OSError:
      if not os.path.isdir(test_results_dir):
        raise

    if not Config.instruments_trace_dir:
      instruments_trace_dir = "/tmp/instruments"
    else:
      instruments_trace_dir = Config.instruments_trace_dir

    return (test_results_dir, instruments_trace_dir)

  def run(self):
    self.run_number += 1
    Log.print_msg("Running test", "{0} ({1} try)".format(self.file_name, number_string_with_postfix(self.run_number)), Colors.CYAN_FG, True)

    (test_results_dir, instruments_trace_dir) = self.__create_folders()
    pipe = OutputPipe(unacceptable_output = [".*Error ?: ?", ".*Fail ?: ?"])
    try:
      app_path = "{0}/{1}/Build/Products/Release-iphonesimulator/{2}.app".format(os.getcwd(), Config.build_dir, self.target.scheme)
      if not os.path.exists(app_path):
        app_path = "{0}/Build/Products/Release-iphonesimulator/{1}.app".format(Config.build_dir, self.target.scheme)
        if not os.path.exists(app_path):
          Log.err("The app does't seem to exist")
          exit(1)
      tests_dir = "{0}/{1}".format(os.getcwd(), Config.tests_dir)
      if not os.path.exists(tests_dir):
        tests_dir = Config.tests_dir
        if not os.path.exists(tests_dir):
          Log.err("The tests directory doesn't seem to exist")
          exit(1)

      inst_cmd = ["instruments",
                  "-D", instruments_trace_dir,
                  "-t", "Automation",
                  "-w", Config.device,
                  "{0}".format(app_path),
                  "-e", "UIASCRIPT", "{0}/{1}".format(tests_dir, self.file_name),
                  "-e", "UIARESULTSPATH", test_results_dir,
                 ]

      if Config.verbose:
        inst_cmd = [inst_cmd[0], "-v"] + inst_cmd[1:]

      ret_code = run_cmd_ret_output(inst_cmd, pipe)
    except TestFailureError:
      ret_code = 1

    self.result = ret_code == 0
    self.output = pipe.meta_lines

