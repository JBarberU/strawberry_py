from sys import stdout

from command_output_pipe_base import CommandOutputPipeBase
from meta_line import MetaLine

class PrettyOutputPipe(CommandOutputPipeBase):

  def __init__(self, pretty = True, unacceptable_output=[]):
    CommandOutputPipeBase.__init__(self, False, unacceptable_output)
    self.meta_lines = []

  def put_line(self, line):
    CommandOutputPipeBase.put_line(self, line)
    self.meta_lines.append(MetaLine(line))
    stdout.write(self.meta_lines[-1].str())


