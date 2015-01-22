import re
from os import getcwd

from command import run_cmd_ret_output
from output_pipe import OutputPipe
from progress_pipe import ProgressPipe
from log import Log

class XCodeBuildBase:

  def __init__(self, target, sdk, build_dir):
    self.target = target
    self.sdk = sdk
    self.build_dir = build_dir

  def build(self, clean, run, device, verbose):
    raise Exception("Unimplemented function")

  @classmethod
  def create_builder(cls, target, sdk, build_dir):
    pipe = OutputPipe(verbose = False)
    run_cmd_ret_output(["xcodebuild", "-version"], pipe)
    version = re.compile("(\d\.?)+").search(pipe.meta_lines[0].body).group()
    if re.compile("6\.*").match(version):
      return XCodeBuild61(target, sdk, build_dir)
    else:
      raise UnsupportedPlatformError("The version {0} is not supported".format(version))

class XCodeBuild61(XCodeBuildBase):
  def build(self, clean, run, device, verbose):
    if verbose:
      pipe_type = OutputPipe
    else:
      pipe_type = ProgressPipe
    if clean:
      Log.msg("Cleaning \"{0}\"".format(self.target.scheme))
      ret_code = run_cmd_ret_output(["xcodebuild",
                                     "clean",
                                     "-sdk", self.sdk,
                                     "-derivedDataPath", self.build_dir,
                                     "-archivePath", self.build_dir,
                                     "-scheme", self.target.scheme],
                                     pipe_type())
      if ret_code != 0:
        return False

    Log.msg("Building \"{0}\"".format(self.target.scheme))
    ret_code = run_cmd_ret_output(["xcodebuild",
                                   "-sdk", self.sdk,
                                   "-derivedDataPath", self.build_dir,
                                   "-archivePath", self.build_dir,
                                   "-scheme", self.target.scheme],
                                   pipe_type())

    if ret_code == 0 and run:
      if not device:
        Log.fatal("Device can't be None")

      ret_code = run_cmd_ret_output(["open", "-a" "/Applications/Xcode.app/Contents/Applications/iOS Simulator.app"], pipe_type())
      if ret_code == 0:
        app_path = "{0}/Build/Products/Release-iphonesimulator/{1}.app".format(self.build_dir, self.target.scheme)
        ret_code = run_cmd_ret_output(["xcrun","simctl", "install", device, app_path], pipe_type())
        if ret_code == 0:
          ret_code = run_cmd_ret_output(["xcrun","simctl", "launch", device, self.target.bundle_id], pipe_type())

    return ret_code == 0



