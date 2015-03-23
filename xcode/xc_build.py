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

  def __init__(self, config):
    self.config = config
    if self.config.debug:
      Log.info("Creating debug builder")

  def build(self, result_formatter):
    raise Exception("Unimplemented function")

  @classmethod
  def create_builder(class_, config):
    pipe = CommandOutputPipeBase(False) # We don't ever want verbose version check 
    commander = Commander(pipe, False)
    commander.run_command(["xcodebuild", "-version"])
    version = re.compile("(\d\.?)+").search(pipe.stdout[0]).group()
    if re.compile("6\.*").match(version):
      return XCodeBuild61(config)
    else:
      raise UnsupportedPlatformError("The version {0} is not supported".format(version))

class XCodeBuild61(XCodeBuildBase):
  def build(self, result_formatter):
    if self.config.verbose:
      pipe_type = PrettyOutputPipe
    else:
      pipe_type = ProgressOutputPipe
    if self.config.clean:
      pipe = pipe_type()
      if result_formatter:
        result_formatter.start(pipe)
      Log.msg("Cleaning \"{0}\"".format(self.config.sel_target.scheme))
      commander = Commander(pipe, self.debug)
      ret_code = commander.run_command(["xcodebuild",
                                     "clean",
                                     "-sdk", self.config.sdk,
                                     "-derivedDataPath", self.config.build_dir,
                                     "-archivePath", self.config.build_dir,
                                     "-configuration", self.target.configuration,
                                     "-scheme", self.config.sel_target.scheme,
                                     ])
      if result_formatter:
        result_formatter.stop(ret_code)
      if ret_code != 0:
        return False

    pipe = pipe_type(self.config.verbose, [])
    if result_formatter:
      result_formatter.start(pipe)
    Log.msg("Building \"{0}\"".format(self.config.sel_target.scheme))
    commander = Commander(pipe, self.config.debug)
    cmd = [
            "xcodebuild",
            "-sdk", self.config.sdk,
            "-derivedDataPath", self.config.build_dir,
            "-archivePath", self.config.build_dir,
            "-configuration", self.config.sel_target.configuration,
            "-scheme", self.config.sel_target.scheme,
            "CODE_SIGN_IDENTITY=\"{0}\"".format(self.config.codesigning_identity)
          ]
    if self.config.provisioning_profile:
      cmd.append("PROVISIONING_PROFILE=\"{0}\"".format(self.config.provisioning_profile))

    ret_code = commander.run_command(cmd)
    if result_formatter:
      result_formatter.stop(ret_code)

    if ret_code == 0 and self.config.run:
      if not self.config.device:
        Log.fatal("Device can't be None")

      ret_code = run_cmd_ret_output(["open", "-a" "/Applications/Xcode.app/Contents/Applications/iOS Simulator.app"], pipe_type())
      if ret_code == 0:
        app_path = get_app_path(self.config.build_dir, self.config.sel_target.configuration, self.config.sel_target.scheme)
        device_booted = False
        time_spent_booting = 0
        while not device_booted and self.sim_boot_timeout > time_spent_booting:
          start = timegm(datetime.utcnow().utctimetuple())
          ret_code = run_cmd_ret_output(["xcrun","simctl", "install", self.config.device, app_path], None)
          if ret_code != 0:
            if time_spent_booting == 0:
              Log.info("Booting Simulator")
            sleep(1)
            time_spent_booting += start - timegm(datetime.utcnow().utctimetuple())
          else:
            device_booted = True

        if ret_code == 0:
          Log.info("Installed {0}".format(self.target.scheme))
          ret_code = run_cmd_ret_output(["xcrun","simctl", "launch", self.config.device, self.config.sel_target.bundle_id], None)
          if ret_code == 0:
            Log.info("Launching {0}".format(self.config.sel_target.scheme))

    return ret_code == 0



