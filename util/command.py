import subprocess
import operator
import sys

from log import Log
from colors import Colors
from strawberry_config import Config

def run_cmd_ret_output(args, formatter):
  cmd = ""
  for a in args:
    cmd += "%s " % a

  if Config.debug:
    Log.msg("Running command: {0}".format(cmd))
  formatter.start()

  p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

  while True:
    line = p.stdout.readline()
    if line != '':
      try:
        formatter.put_line(line)
      except RuntimeError as e:
        p.terminate()
        raise e
    else:
      break
  p.wait()
  formatter.stop()
  return p.returncode

