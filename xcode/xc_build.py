import re
from os import getcwd
from datetime import datetime
from calendar import timegm
from time import sleep

from command import run_cmd_ret_output
from output_pipe import OutputPipe
from pretty_pipe import PrettyPipe
from progress_pipe import ProgressPipe
from log import Log

class XCodeBuildBase:

  sim_boot_timeout = 10

  def __init__(self, target, sdk, build_dir):
    self.target = target
    self.sdk = sdk
    self.build_dir = build_dir

  def build(self, clean, run, device, verbose):
    raise Exception("Unimplemented function")

  @classmethod
  def create_builder(cls, target, sdk, build_dir):
    pipe = OutputPipe()
    run_cmd_ret_output(["xcodebuild", "-version"], pipe)
    version = re.compile("(\d\.?)+").search(pipe.meta_lines[0].body).group()
    if re.compile("6\.*").match(version):
      return XCodeBuild61(target, sdk, build_dir)
    else:
      raise UnsupportedPlatformError("The version {0} is not supported".format(version))

class XCodeBuild61(XCodeBuildBase):
  def build(self, clean, run, device, result_formatter, verbose):
    if verbose:
      pipe_type = PrettyPipe
    else:
      pipe_type = ProgressPipe
    if clean:
      pipe = pipe_type()
      if result_formatter:
        result_formatter.start(pipe)
      Log.msg("Cleaning \"{0}\"".format(self.target.scheme))
      ret_code = run_cmd_ret_output(["xcodebuild",
                                     "clean",
                                     "-sdk", self.sdk,
                                     "-derivedDataPath", self.build_dir,
                                     "-archivePath", self.build_dir,
                                     "-scheme", self.target.scheme],
                                     pipe)
      if result_formatter:
        result_formatter.stop(ret_code)
      if ret_code != 0:
        return False

    pipe = pipe_type()
    if result_formatter:
      result_formatter.start(pipe)
    Log.msg("Building \"{0}\"".format(self.target.scheme))
    ret_code = run_cmd_ret_output(["xcodebuild",
                                   "-sdk", self.sdk,
                                   "-derivedDataPath", self.build_dir,
                                   "-archivePath", self.build_dir,
                                   "-scheme", self.target.scheme],
                                   pipe)
    if result_formatter:
      result_formatter.stop(ret_code)

    if ret_code == 0 and run:
      if not device:
        Log.fatal("Device can't be None")

      ret_code = run_cmd_ret_output(["open", "-a" "/Applications/Xcode.app/Contents/Applications/iOS Simulator.app"], pipe_type())
      if ret_code == 0:
        app_path = "{0}/Build/Products/Release-iphonesimulator/{1}.app".format(self.build_dir, self.target.scheme)
        device_booted = False
        time_spent_booting = 0
        while not device_booted and self.sim_boot_timeout > time_spent_booting:
          start = timegm(datetime.utcnow().utctimetuple())
          ret_code = run_cmd_ret_output(["xcrun","simctl", "install", device, app_path], None)
          if ret_code != 0:
            if time_spent_booting == 0:
              Log.info("Booting Simulator")
            sleep(1)
            time_spent_booting += start - timegm(datetime.utcnow().utctimetuple())
          else:
            device_booted = True

        if ret_code == 0:
          Log.info("Installed {0}".format(self.target.scheme))
          ret_code = run_cmd_ret_output(["xcrun","simctl", "launch", device, self.target.bundle_id], None)
          if ret_code == 0:
            Log.info("Launching {0}".format(self.target.scheme))

    return ret_code == 0



