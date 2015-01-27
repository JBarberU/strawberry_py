import sys
import re
from output_pipe_base import OutputPipeBase
from meta_line import MetaLine

class OutputPipe(OutputPipeBase):
  meta_lines = []

# unacceptable_output is usful for failing based on command output, rather than
# exitcode
  def __init__(self, verbose = True, unacceptable_output=[]):
    OutputPipeBase.__init__(self, verbose, unacceptable_output)
    self.meta_lines = []

  def put_line(self, line):
    OutputPipeBase.put_line(self, line)
    m_line = MetaLine(line)
    self.meta_lines.append(m_line)

  def start(self):
    pass

  def stop(self):
    pass

