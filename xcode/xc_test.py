from colors import Colors
from os import mkdir, listdir
from shutil import rmtree
import random
from strawberry_config import Config
from log import Log
from command import run_cmd_ret_output

class TestCase:
  result = False
  file_name = ""
  target = None
  time_spent = ""
  output = []

  def __init__(self, file_name_in, target):
    self.file_name = file_name_in
    self.target = target

  def run(self):
    print("Running test: %s" % self.file_name)

    result_dir = "result_dir-%032x" % random.getrandbits(128)
    mkdir(result_dir)
    instruments_trace = "instruments_trace-%032x" % random.getrandbits(128)
    mkdir(instruments_trace)
    (ret_code, lines) = run_cmd_ret_output(["instruments", 
                                            "-v",
                                            "-D", instruments_trace, 
                                            "-t", "Automation", 
                                            "-w", "iPhone 5s (8.1 Simulator",
                                            "%s/Build/Products/Release-iphonesimulator/%s.app" % 
                                              (Config.build_dir, self.target.scheme),
                                            "-e", "UIASCRIPT", "%s/%s" %(Config.tests_dir, self.file_name),
                                            "-e", "UIARESULTSPATH", result_dir,
                                           ], True)
    rmtree(instruments_trace)
    self.result = ret_code
    self.output = lines

class ResultFormatterBase:
  def format_result(self, test_cases):
    print("BaseFormatter doesn't know what to do :(")

class CommandlineResultFormatter(ResultFormatterBase):

  def format_result(self, test_cases):
    for tc in test_cases:
      if tc.result:
        Log.msg("%s passed" % tc.file_name)
      else:
        Log.err("%s failed" % tc.file_name)

def test(target, sdk, focus=[], verbose=True):
  try:
    tests_dir = Config.tests_dir
  except AttributeError:
    tests_dir =  "integration/javascript/iPhone" 
    Log.warn("tests_dir not set, defaulting to: %s" % tests_dir)

  test_files = listdir(tests_dir)
  tests = []
  for tf in test_files:
    tests.append(TestCase(tf, target))
    
#  tests[0].run()
  for tc in tests:
    tc.run()

  formatter = CommandlineResultFormatter()
  formatter.format_result(tests)


