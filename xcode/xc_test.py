from os import listdir
from strawberry_config import Config
from xc_testcase import TestCase
from commandline_formatter import CommandlineResultFormatter
from junit_formatter import JUnitResultFormatter


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
    
  tests[4].run()
#  for tc in tests:
#    tc.run()

  formatter = JUnitResultFormatter()
  lines = formatter.format_result(tests)
  with open(Config.report_file, "w") as f:
    f.writelines(lines)




