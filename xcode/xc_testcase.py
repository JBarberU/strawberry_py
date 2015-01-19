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
      test_results_dir = "%s/results" % tempfile.gettempdir()#, random.getrandbits(128))
    else:
      test_results_dir = Config.test_results_dir

    try:
      os.makedirs(test_results_dir)
    except OSError:
      if not os.path.isdir(test_results_dir):
        raise

    if not Config.instruments_trace_dir:
      instruments_trace_dir = "%s/instruments" % tempfile.gettempdir()
    else:
      instruments_trace_dir = Config.instruments_trace_dir

    try:
      os.makedirs(instruments_trace_dir)
    except OSError:
      if not os.path.isdir(instruments_trace_dir):
        raise

    return (test_results_dir, instruments_trace_dir)

  def run(self):
    self.run_number += 1
    Log.print_msg("Running test", "{0} ({1} try)".format(self.file_name, number_string_with_postfix(self.run_number)), Colors.CYAN_FG, True)

    (test_results_dir, instruments_trace_dir) = self.__create_folders()
    pipe = OutputPipe(unacceptable_output = [".*Error ?: ?", ".*Fail ?: ?"])
    try:
      ret_code = run_cmd_ret_output(["instruments",
                                     #"-v",
                                     "-D", instruments_trace_dir,
                                     "-t", "Automation",
                                     "-w", "{0}".format(Config.device),
                                     "%s/Build/Products/Release-iphonesimulator/%s.app" %
                                       (Config.build_dir, self.target.scheme),
                                     "-e", "UIASCRIPT", "%s/%s" %(Config.tests_dir, self.file_name),
                                     "-e", "UIARESULTSPATH", test_results_dir,
                                    ], pipe)
    except TestFailureError:
      ret_code = 1

    self.result = ret_code == 0
    self.output = pipe.meta_lines

