import re
from os import getcwd
from datetime import datetime
from calendar import timegm
from time import sleep

from commander import Commander
from command_output_pipe_base import CommandOutputPipeBase
from pretty_output_pipe import PrettyOutputPipe
from progress_output_pipe import ProgressOutputPipe
from log import Log
from xc_utils import get_app_path

class XCodeBuildBase:

  sim_boot_timeout = 10

  def __init__(self, target, sdk, build_dir, debug):
    self.target = target
    self.sdk = sdk
    self.build_dir = build_dir
    self.debug = debug

  def build(self, clean, run, device, result_formatter, verbose):
    raise Exception("Unimplemented function")

  @classmethod
  def create_builder(class_, target, sdk, build_dir, debug = False, verbose = False):
    pipe = CommandOutputPipeBase(verbose)
    commander = Commander(pipe, debug)
    commander.run_command(["xcodebuild", "-version"])
    version = re.compile("(\d\.?)+").search(pipe.stdout[0]).group()
    if re.compile("6\.*").match(version):
      return XCodeBuild61(target, sdk, build_dir, debug, verbose)
    else:
      raise UnsupportedPlatformError("The version {0} is not supported".format(version))

class XCodeBuild61(XCodeBuildBase):
  def build(self, clean, run, device, result_formatter, verbose):
    if verbose:
      pipe_type = PrettyPipe
    else:
      pipe_type = ProgressOutputPipe
    if clean:
      pipe = pipe_type()
      if result_formatter:
        result_formatter.start(pipe)
      Log.msg("Cleaning \"{0}\"".format(self.target.scheme))
      commander = Commander(pipe, self.debug)
      ret_code = commander.run_command(["xcodebuild",
                                     "clean",
                                     "-sdk", self.sdk,
                                     "-derivedDataPath", self.build_dir,
                                     "-archivePath", self.build_dir,
                                     "-configuration", self.target.configuration,
                                     "-scheme", self.target.scheme,
                                     ])
      if result_formatter:
        result_formatter.stop(ret_code)
      if ret_code != 0:
        return False

    pipe = pipe_type()
    if result_formatter:
      result_formatter.start(pipe)
    Log.msg("Building \"{0}\"".format(self.target.scheme))
    commander = Commander(pipe)
    ret_code = commander.run_command(["xcodebuild",
                                   "-sdk", self.sdk,
                                   "-derivedDataPath", self.build_dir,
                                   "-archivePath", self.build_dir,
                                   "-configuration", self.target.configuration,
                                   "-scheme", self.target.scheme])
    if result_formatter:
      result_formatter.stop(ret_code)

    if ret_code == 0 and run:
      if not device:
        Log.fatal("Device can't be None")

      ret_code = run_cmd_ret_output(["open", "-a" "/Applications/Xcode.app/Contents/Applications/iOS Simulator.app"], pipe_type())
      if ret_code == 0:
        app_path = get_app_path(self.build_dir, self.target.configuration, self.target.scheme)
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



