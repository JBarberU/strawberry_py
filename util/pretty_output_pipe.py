from sys import stdout

from output_error import OutputError
from command_output_pipe_base import CommandOutputPipeBase
from meta_line import MetaLine

class PrettyOutputPipe(CommandOutputPipeBase):

  def __init__(self, verbose = False, unacceptable_output=[]):
    CommandOutputPipeBase.__init__(self, verbose, unacceptable_output)
    self.meta_lines = []

  def put_line(self, line):
    try:
      CommandOutputPipeBase.put_line(self, line)
    except OutputError, e:
      raise e
    finally:
      self.meta_lines.append(MetaLine(line))
      stdout.write(self.meta_lines[-1].str())

  def put_error_line(self, line):
    try:
      CommandOutputPipeBase.put_error_line(self, line)
    except OutputError, e:
      raise e
    finally:
      self.meta_lines.append(MetaLine(line))
      stdout.write(self.meta_lines[-1].str())

