import readline
import sys
import shutil
import os

from log import Log

def get_var(msg, default):
  sys.stdout.write("%s (default is \"%s\"): " % (msg, default))
  ret = raw_input()
  if ret == "":
    return default
  return ret

def setup():
  if not os.path.exists("strawberry_config.py"):
    sys.stdout.write("You're missing strawberry_config.py at %s, do you want to create it? Y/N: " % os.getcwd())
    ans = raw_input()
    if ans == "y" or ans == "Y":
      shutil.copy("%s/../strawberry_config.py.sample" % os.path.dirname(__file__), "strawberry_config.py")
      Log.info("Created strawberry_config.py, edit it to suit your needs")
    else:
      Log.err("Didn't create strawberry_config.py, you won't be able to use strawberry_py until you do")
  else:
    Log.info("strawberry_config.py already exists, nothing to do...")



