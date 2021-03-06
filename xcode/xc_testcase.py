import os
import random
import tempfile

from number_helper import number_string_with_postfix
from output_error import OutputError
from pretty_output_pipe import PrettyOutputPipe
from commander import Commander
from xc_config import Config
from shutil import rmtree
from log import Log
from colors import Colors
from xc_utils import get_app_path

class TestCase:
  result = False
  file_name = ""
  target = None
  time_spent = ""
  output = []
  run_number = 0

  def __init__(self, file_name_in, config):
    self.file_name = file_name_in
    self.config = config

  def __create_folders(self):
    if not self.config.test_results_dir:
      test_results_dir = "/tmp/results"
    else:
      test_results_dir = self.config.test_results_dir

    try:
      os.makedirs(test_results_dir)
    except OSError:
      if not os.path.isdir(test_results_dir):
        raise

    if not self.config.instruments_trace_dir:
      instruments_trace_dir = "/tmp/instruments"
    else:
      instruments_trace_dir = self.config.instruments_trace_dir

    return (test_results_dir, instruments_trace_dir)

  def run(self):
    if len(self.config.sel_targets) > 1:
      Log.err("Running tests for multiple targets is currintly unsupported")
      return

    self.run_number += 1
    Log.print_msg("Running test", "{0} ({1} try)".format(self.file_name, number_string_with_postfix(self.run_number)), Colors.CYAN_FG, True)

    (test_results_dir, instruments_trace_dir) = self.__create_folders()
    pipe = PrettyOutputPipe(unacceptable_output = [".*Error ?: ?", ".*Fail ?: ?"])
    try:
      app_path = get_app_path(self.config, self.config.sel_targets[0])
      if not os.path.exists(app_path):
        Log.err("The app does't seem to exist")
        exit(1)
      tests_dir = "{0}/{1}".format(os.getcwd(), self.config.tests_dir)
      if not os.path.exists(tests_dir):
        tests_dir = self.config.tests_dir
        if not os.path.exists(tests_dir):
          Log.err("The tests directory doesn't seem to exist")
          exit(1)

      inst_cmd = ["instruments",
                  "-D", instruments_trace_dir,
                  "-t", "Automation",
                  "-w", self.config.device,
                  "{0}".format(app_path),
                  "-e", "UIASCRIPT", "{0}/{1}".format(tests_dir, self.file_name),
                  "-e", "UIARESULTSPATH", test_results_dir,
                 ]

      if self.config.verbose:
        inst_cmd = [inst_cmd[0], "-v"] + inst_cmd[1:]

      commander = Commander(pipe, self.config.debug)
      ret_code = commander.run_command(inst_cmd)
    except OutputError:
      ret_code = 1

    self.result = ret_code == 0
    self.output = pipe.meta_lines

