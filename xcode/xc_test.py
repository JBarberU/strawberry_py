from os import listdir
from operator import contains
from strawberry_config import Config
from xc_testcase import TestCase
from commandline_formatter import CommandlineResultFormatter
from junit_formatter import JUnitResultFormatter
from text_formatter import TextResultFormatter
from command import run_cmd_ret_output
from progress_pipe import ProgressPipe
from pretty_pipe import PrettyPipe
from log import Log

class TestObjectBase:

  def fix_js_extension(self, file_list):
    ret = []
    for f in file_list:
      if f[-3:] == ".js":
        ret += [f]
      else:
        ret += ["%s.js" % f]

    return ret

  def get_tests(self, tests):
    pass

class TestExcludeObject(TestObjectBase):

  def __init__(self, exclude):
    self.exclude = self.fix_js_extension(exclude)

  def get_tests(self, tests):
    ret = []
    for t in tests:
      if not contains(self.exclude, t.file_name):
        ret.append(t)

    return ret

class TestFocusObject(TestObjectBase):

  def __init__(self, focus):
    self.focus = self.fix_js_extension(focus)

  def get_tests(self, tests):
    ret = []
    for t in tests:
      if contains(self.focus, t.file_name):
        ret.append(t)

    return ret

formatter_map = {
                  'junit': JUnitResultFormatter,
                  'text': TextResultFormatter,
                }

def test(target, sdk, focus_object=None, retry_count=1, reinstall=False, verbose=True):
  try:
    tests_dir = Config.tests_dir
  except AttributeError:
    tests_dir =  "integration/javascript/iphone"
    Log.warn("tests_dir not set, defaulting to: %s" % tests_dir)

  test_files = listdir(tests_dir)
  tests = []
  for tf in test_files:
    tests.append(TestCase(tf, target))

  if focus_object:
    tests = focus_object.get_tests(tests)

  if Config.debug:
    pipe_type = PrettyPipe
  else:
    pipe_type = ProgressPipe

  for tc in tests:
    for i in range(retry_count):
      if reinstall:
        ret_code = run_cmd_ret_output(["xcrun","simctl", "uninstall", Config.device, target.bundle_id], pipe_type())
        if not (ret_code == 0 or ret_code == 1):
          Log.err("Uninstall failed!")
      tc.run()
      if tc.result:
        break

  if Config.test_report_format:
    formatter = formatter_map[Config.test_report_format]()
    lines = formatter.format_result(tests)
    if Config.test_report_file[-len(formatter.file_extension):] != formatter.file_extension:
      file_name = "%s.%s" % (Config.test_report_file, formatter.file_extension)
    else:
      file_name = Config.test_report_file

    with open(file_name, "w") as f:
      f.writelines(lines)




