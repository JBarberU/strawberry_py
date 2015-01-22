from sys import stdout

from output_pipe import OutputPipe

class PrettyPipe(OutputPipe):

  def __init__(self, pretty = True, unacceptable_output=[]):
    OutputPipe.__init__(self, unacceptable_output)
    self.pretty = pretty

  def put_line(self, line):
    OutputPipe.put_line(self, line)
    if self.pretty:
      output = self.meta_lines[-1].str()
    else:
      output = line

    stdout.write(output)


