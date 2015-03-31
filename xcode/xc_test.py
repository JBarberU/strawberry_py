from os import listdir
from operator import contains
from xc_config import Config
from xc_testcase import TestCase
from xc_utils import get_app_path
from commandline_formatter import CommandlineResultFormatter
from junit_formatter import JUnitResultFormatter
from text_formatter import TextResultFormatter
from commander import Commander
from progress_output_pipe import ProgressOutputPipe
from pretty_output_pipe import PrettyOutputPipe
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

def test(config):
  if len(config.sel_targets) > 1:
    Log.err("There isn't currently any support for running tests with multiple targets")
    return 

  if config.focus:
    focus_object = TestFocusObject(config.focus)
  elif config.exclude:
    focus_object = TestExcludeObject(config.exclude)
  else:
    focus_object = None

  try:
    tests_dir = config.tests_dir
  except AttributeError:
    tests_dir =  "integration/javascript/iphone"
    Log.warn("tests_dir not set, defaulting to: %s" % tests_dir)

  test_files = listdir(tests_dir)
  tests = []
  for tf in test_files:
    tests.append(TestCase(tf, config))

  if focus_object:
    tests = focus_object.get_tests(tests)

  if config.debug:
    pipe_type = PrettyOutputPipe
  else:
    pipe_type = ProgressOutputPipe

  for tc in tests:
    for i in range(config.retry_count):
      if config.reinstall:
        commander = Commander(pipe_type(), debug)
        explicit_boot = commander.run_command(["xcrun","simctl", "boot", config.device])

        ret_code = commander.run_command(["xcrun","simctl", "uninstall", config.device, target.bundle_id])
        if not (ret_code == 0 or ret_code == 1):
          Log.err("Uninstall failed!")
        ret_code = commander.run_command(["xcrun","simctl", "install", config.device, get_app_path(config, config.sel_targets[0])])
        if not (ret_code == 0 or ret_code == 1):
          Log.fatal("Install failed! error code: {}".format(ret_code))

        if explicit_boot == 0:
          # explicit_boot != 0 implies that the device was booted by instuments
          # and should be kept alive
          ret_code = commander.run_command(["xcrun","simctl", "shutdown", config.device])

      tc.run()
      if tc.result:
        break

  if config.test_report_format:
    formatter = formatter_map[config.test_report_format]()
    lines = formatter.format_result(tests)
    if config.test_report_file[-len(formatter.file_extension):] != formatter.file_extension:
      file_name = "%s.%s" % (config.test_report_file, formatter.file_extension)
    else:
      file_name = config.test_report_file

    with open(file_name, "w") as f:
      f.writelines(lines)




