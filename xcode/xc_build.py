import re

from command import run_cmd_ret_output
from output_pipe import OutputPipe

class XCodeBuildBase:
  def build(self, clean, target, sdk, run, verbose):
    raise Exception("Unimplemented function")

  @classmethod
  def create_builder(cls):
    pipe = OutputPipe()
    run_cmd_ret_output(["xcodebuild", "-version"], pipe)
    version = re.compile("(\d\.?)+").search(pipe.meta_lines[0].body).group()
    if re.compile("6\.*").match(version):
      return XCodeBuild61()
    else:
      raise UnsupportedPlatformError("The version {0} is not supported".format(version))

class XCodeBuild61(XCodeBuildBase):
  def build(self, clean, target, sdk, run, verbose):
    pipe = OutputPipe()
    if clean:
      ret_code = run_cmd_ret_output(["xcodebuild",
                                     "clean",
                                     "-sdk", sdk,
                                     "-scheme", target.scheme],
                                     pipe)
      if ret_code != 0:
        return False

    ret_code = run_cmd_ret_output(["xcodebuild",
                                   "-sdk", sdk,
                                   "-scheme", target.scheme],
                                   pipe)

    return ret_code == 0

