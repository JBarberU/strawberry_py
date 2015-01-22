import re
from os import getcwd

from command import run_cmd_ret_output
from output_pipe import OutputPipe
from progress_pipe import ProgressPipe
from log import Log

class XCodeBuildBase:
  def build(self, clean, target, sdk, run, verbose):
    raise Exception("Unimplemented function")

  @classmethod
  def create_builder(cls):
    pipe = OutputPipe(verbose = False)
    run_cmd_ret_output(["xcodebuild", "-version"], pipe)
    version = re.compile("(\d\.?)+").search(pipe.meta_lines[0].body).group()
    if re.compile("6\.*").match(version):
      return XCodeBuild61()
    else:
      raise UnsupportedPlatformError("The version {0} is not supported".format(version))

class XCodeBuild61(XCodeBuildBase):
  def build(self, clean, target, sdk, build_dir, run, verbose):
    if verbose:
      pipe_type = OutputPipe
    else:
      pipe_type = ProgressPipe
    if clean:
      Log.msg("Cleaning \"{0}\"".format(target.scheme))
      ret_code = run_cmd_ret_output(["xcodebuild",
                                     "clean",
                                     "-sdk", sdk,
                                     "-derivedDataPath", build_dir,
                                     "-archivePath", build_dir,
                                     "-scheme", target.scheme],
                                     pipe_type())
      if ret_code != 0:
        return False

    Log.msg("Building \"{0}\"".format(target.scheme))
    ret_code = run_cmd_ret_output(["xcodebuild",
                                   "-sdk", sdk,
                                   "-derivedDataPath", build_dir,
                                   "-archivePath", build_dir,
                                   "-scheme", target.scheme],
                                   pipe_type())

    if ret_code == 0 and run:
      ret_code = run_cmd_ret_output(["open", "-a" "/Applications/Xcode.app/Contents/Applications/iOS Simulator.app"], pipe_type())
      if ret_code == 0:
        app_path = "{0}/Build/Products/Release-iphonesimulator/{1}.app".format(build_dir, self.target.scheme)
        ret_code = run_cmd_ret_output(["xcrun","simctl", "install", Config.device, app_path], pipe_type())

    return ret_code == 0



