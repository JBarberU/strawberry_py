from output_pipe import OutputPipe
from command import run_cmd_ret_output
from strawberry_config import Config
from shutil import rmtree
from os import mkdir
import random

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
    pipe = OutputPipe()
    ret_code = run_cmd_ret_output(["instruments", 
                                   #"-v",
                                   "-D", instruments_trace, 
                                   "-t", "Automation", 
                                   "-w", "iPhone 5s (8.1 Simulator",
                                   "%s/Build/Products/Release-iphonesimulator/%s.app" % 
                                     (Config.build_dir, self.target.scheme),
                                   "-e", "UIASCRIPT", "%s/%s" %(Config.tests_dir, self.file_name),
                                   "-e", "UIARESULTSPATH", result_dir,
                                  ], pipe)
    rmtree("%s.trace" % instruments_trace)
    rmtree(result_dir)
    self.result = ret_code == 0
    self.output = pipe.meta_lines


