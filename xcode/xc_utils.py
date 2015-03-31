import re
from os import path
from commander import Commander
from command_output_pipe_base import CommandOutputPipeBase
from log import Log

def get_device(device_name, debug=False):
  pipe = CommandOutputPipeBase(False)
  commander = Commander(pipe, debug)
  ret_code = commander.run_command(["instruments", "-s", "devices"])
  for line in pipe.stdout:
    search = re.compile(re.escape(device_name)).match(line)
    if search:
      b, e = re.compile("\[[0-9a-fA-F-]+]").search(line).span()
      return line[b+1:e-1]

  return ""

def get_app_path(config, target):
  is_simulator = sdk_regex = re.compile(".*simulator.*").match(config.sdk)
  __paths = [
              "{0}/Build/Products/{1}-{2}/{3}.{4}",
              "{0}/Products/{1}-{2}/{3}.{4}",
            ]

  Log.info("sdk: {0}".format(config.sdk))

  paths_tried = []
  for p in __paths:
    app_path = p.format(config.build_dir, target.configuration, "iphonesimulator" if is_simulator else "iphoneos", target.app_name, config.export_format)
    paths_tried.append(app_path)
    if config.debug:
      Log.info("Looking for {0} in {1}".format(target.app_name, app_path))
    if path.exists(app_path):
      return app_path

  raise RuntimeError("Unable to find {0} in {1}".format(target.app_name, ",".join(paths_tried)))

