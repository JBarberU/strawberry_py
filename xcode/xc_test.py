from os import listdir
from operator import contains
from strawberry_config import Config
from xc_testcase import TestCase
from commandline_formatter import CommandlineResultFormatter
from junit_formatter import JUnitResultFormatter

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


def test(target, sdk, focus_object=None, verbose=True):
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
    
  for tc in tests:
    tc.run()

  formatter = JUnitResultFormatter()
  lines = formatter.format_result(tests)
  with open(Config.test_report_file, "w") as f:
    f.writelines(lines)




