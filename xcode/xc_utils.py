import re
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

