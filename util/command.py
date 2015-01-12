import subprocess
import operator  
import sys

from colors import Colors

def run_cmd(args, verbose, show_progress=False, acceptable_error_codes=[0]):
  if not operator.contains(acceptable_error_codes, 0):
    acceptable_error_codes.append(0)

  cmd = ""
  for a in args:
    cmd += "%s " % a

  print("%sRunning command: %s%s" % (Colors.GREEN, Colors.NORMAL, cmd))
  p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  if show_progress:
    sys.stdout.write("%sRunning%s" % (Colors.BLUE, Colors.NORMAL))

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
    sys.stdout.write("%sDone!%s" % (Colors.BLUE, Colors.NORMAL))
    print("")
  p.wait()
  if p.returncode != 0:
    if not operator.contains(acceptable_error_codes, p.returncode):
      print("%sError:%s Command \"%s\" exited with code: %s" % (Colors.RED, Colors.NORMAL, cmd, p.returncode))
      exit(1)
    else:
      print("%sWarning:%s Command \"%s\" exited with code: %s" % (Colors.YELLOW, Colors.NORMAL, cmd, p.returncode))

