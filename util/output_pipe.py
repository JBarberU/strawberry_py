import sys
from colors import Colors
from meta_line import MetaLine
from line import Line

class OutputPipe:
  meta_lines = []
  verbose = True
  pretty = True

  def __init__(self, verbose = True, pretty = True):
    self.verbose = verbose
    self.pretty = pretty

  def put_line(self, line):
    m_line = MetaLine(line)
    self.meta_lines.append(m_line)

    if self.verbose:
      if self.pretty:
        output = m_line.str()
      else:
        output = line

      sys.stdout.write(output)

