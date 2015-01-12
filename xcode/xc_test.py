from colors import Colors
from os import walk, listdir
from strawberry_config import Config
from log import Log

def test(target, sdk, focus=[], verbose=True):
  try:
    tests_dir = Config.tests_dir
  except AttributeError:
    tests_dir =  "integration/javascript/iPhone" 
    Log.warn("tests_dir not set, defaulting to: %s" % tests_dir)

  test_files = listdir(tests_dir)
  for tf in test_files:
    print("tf: %s" % tf)
  Log.msg("Running tests :)")

