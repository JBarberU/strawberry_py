import subprocess
import operator  
import sys

from log import Log
from colors import Colors 

def run_cmd_ret_output(args, verbose):
  p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  lines = []

  while True:
    line = p.stdout.readline()
    if line != '':
      if verbose:
        sys.stdout.write(line)

      lines.append(line)
    else:
      break
  p.wait()
  return (p.returncode, lines)

def run_cmd(args, verbose, show_progress=False, acceptable_error_codes=[0]):
  if not operator.contains(acceptable_error_codes, 0):
    acceptable_error_codes.append(0)

  cmd = ""
  for a in args:
    cmd += "%s " % a

  Log.print_msg("Running command", cmd, Colors.GREEN)
  p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  if show_progress:
    sys.stdout.write("%sRunning%s: " % (Colors.BLUE, Colors.NORMAL))

  while True:
    line = p.stdout.readline()
    if line != '':
      if verbose:
        print line
      elif show_progress:
        sys.stdout.write("%s.%s" % (Colors.BLUE, Colors.NORMAL))
    else:
      break
  if show_progress:
    sys.stdout.write("%s Done!%s" % (Colors.NORMAL, Colors.NORMAL))
    print("")
  p.wait()
  if p.returncode != 0:
    if not operator.contains(acceptable_error_codes, p.returncode):
      Log.err("Command \"%s\" exited with code: %s" % (cmd, p.returncode))
      exit(1)
    else:
      Log.warn("Command \"%s\" exited with code: %s" % (cmd, p.returncode))

