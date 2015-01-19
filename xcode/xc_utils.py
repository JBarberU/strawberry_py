import re
from command import run_cmd_ret_output
from output_pipe import OutputPipe

def get_device(device_name):
  pipe = OutputPipe(verbose = False)
  ret_code = run_cmd_ret_output(["instruments", "-s", "devices"], pipe)
  for m_line in pipe.meta_lines:
    search = re.compile(re.escape(device_name)).match(m_line.body)
    if search:
      b, e = re.compile("\[[0-9a-fA-F-]+]").search(m_line.body).span()
      return m_line.body[b+1:e-1]

  return ""

