from build_formatter_base import BuildFormatterBase

class BuildXMLFormatter(BuildFormatterBase):

  def __init__(self, file_name):
    BuildFormatterBase.__init__(self)
    self.file_name = file_name
    self.builds = []

  def start(self, pipe):
    BuildFormatterBase.start(self, pipe)

  def stop(self, return_code):
    BuildFormatterBase.stop(self, return_code)

    lines = []
    for l in self.pipe.stdout:
      lines.append(l)

    self.builds.append((lines, return_code))

  def save(self):
    BuildFormatterBase.save(self)

    with open(self.file_name, "w") as f:
      f.write("<session>\n")
      for (b, rc) in self.builds:
        f.write("<\tbuild return_code=\"{0}\">\n".format(rc))
        f.write("\t\t<build_log>\n")
        for l in b:
          if l[-1] == "\n":
            line = l
          else:
            line = "{0}\n".format(l)
          f.write("\t\t\t{0}".format(line))
        f.write("\t\t</build_log>\n")
        f.write("\t</build>\n")
      f.write("</session>\n")


