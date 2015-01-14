from colors import Colors
from line import Line
import re

prefixes = [
            ("Start", "", Colors.GREEN),
            ("Pass", "", Colors.GREEN),
            ("Debug", "", Colors.BLUE),
            ("Error", "", Colors.RED),
            ("Fail", "", Colors.RED),
            ("Duration", "s;", Colors.BLUE),
            ("logElementTree", "", Colors.BLUE),
           ]

class MetaLine(Line):
  color = Colors.NORMAL
  prefix = ""
  body = ""

  def __init__(self, line):
    self.body = line
    for (p, end, c) in prefixes:
      match = re.compile(".*%s ?: ?" % p).match(line)
      if match:
        self.color = c
        self.prefix = p
        (_, index) = match.span()
        body = line[index:]

        if end != "":
          index = body.find(end)
          if index != -1:
            body = body[:index]
            body += "\n"

        self.body = body
        break

  def str(self):
    return "%s%s%s: %s" % (self.color, self.prefix, Colors.NORMAL, self.body)

