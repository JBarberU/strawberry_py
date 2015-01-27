import re
from os import path
from commander import Commander
from command_output_pipe_base import CommandOutputPipeBase

def get_device(device_name):
  pipe = CommandOutputPipeBase(False)
  commander = Commander(pipe)
  ret_code = commander.run_command(["instruments", "-s", "devices"])
  for line in pipe.stdout:
    search = re.compile(re.escape(device_name)).match(line)
    if search:
      b, e = re.compile("\[[0-9a-fA-F-]+]").search(line).span()
      return line[b+1:e-1]

  return ""

def get_app_path(build_dir, scheme):
  __paths = [
              "{0}/Build/Products/Release-iphonesimulator/{1}.app",
              "{0}/Products/Release-iphonesimulator/{1}.app",
            ]

  for p in __paths:
    app_path = p.format(build_dir, scheme)
    if path.exists(app_path):
      return app_path

  raise RuntimeError("Unable to find {0}.app".format(scheme))

