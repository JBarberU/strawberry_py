import json
from log import Log
from xc_target import Target

class Config:

  def __init__(self, config_file):
    if config_file:
      with open(config_file, "r") as f:
        json_root = json.load(f)
    else:
      json_root = {}

    self.deserialize(json_root)

  def save(self, file_path):
    with open(file_path, "w") as f:
      f.write(json.dumps(self.serialize(), sort_keys=True, indent=2, separators=(',',': ')))

  def serialize(self):
    print("serialize")
    json_object = {
      "tests_dir": self.tests_dir,
      "build_dir": self.build_dir,
      "build_report_format": self.build_report_format,
      "build_report_file": self.build_report_file,
      "test_report_format": self.test_report_format,
      "test_report_file": self.test_report_file,
      "test_results_dir": self.test_results_dir,
      "instruments_trace_dir": self.instruments_trace_dir,
      "device": self.device,
      "clean": self.clean,
      "target": self.target,
      "sdk": self.sdk,
      "run": self.run,
      "build": self.build,
      "test": self.test,
      "focus": self.focus,
      "exclude": self.exclude,
      "retry_count": self.retry_count,
      "reinstall": self.reinstall,
      "verbose": self.verbose,
      "debug": self.debug,
      "foo": self.foo,
      "targets": Target.serialize(self.targets)
    }

    return json_object

  def deserialize(self, json_object):
    print("deserialize")
    self.init_mem(json_object, "tests_dir",             "integration/javascript/iphone")
    self.init_mem(json_object, "build_dir",             "build")
    self.init_mem(json_object, "build_report_format",   "xml")
    self.init_mem(json_object, "build_report_file",     "build-report.xml")
    self.init_mem(json_object, "test_report_format",    "junit")
    self.init_mem(json_object, "test_report_file",      "test-report.xml")
    self.init_mem(json_object, "test_results_dir",      "test_results")
    self.init_mem(json_object, "instruments_trace_dir", "instruments")
    self.init_mem(json_object, "device",                None)
    self.init_mem(json_object, "clean",                 False)
    self.init_mem(json_object, "target",                None)
    self.init_mem(json_object, "sdk",                   "iphoneos8.1")
    self.init_mem(json_object, "run",                   False)
    self.init_mem(json_object, "build",                 True)
    self.init_mem(json_object, "test",                  True)
    self.init_mem(json_object, "focus",                 None)
    self.init_mem(json_object, "exclude",               None)
    self.init_mem(json_object, "retry_count",           1)
    self.init_mem(json_object, "reinstall",             False)
    self.init_mem(json_object, "verbose",               False)
    self.init_mem(json_object, "debug",                 False)
    self.init_mem(json_object, "foo",                   "bar")

    try:
      self.targets = Target.deserialize(json_object["targets"])
    except KeyError:
      self.targets = self.example_targets

  def init_mem(self, json_object, key, default):
    try:
      value = json_object[key]
    except KeyError:
      value = default
    setattr(self, key, value)

  example_targets = [
    Target(name="foo",
           scheme="Foo Scheme",
           app_name="Foo.app",
           configuration="Debug",
           bundle_id="com.example.MyApp-Foo"),
    Target(name="bar",
           scheme="Bar Scheme",
           app_name= "Bar.app",
           configuration="Release",
           bundle_id="com.example.MyApp-Bar"),
    Target(name="bar_debug",
           scheme="Bar Scheme",
           app_name= "Bar.app",
           configuration="Debug",
           bundle_id="com.example.MyApp-Bar")
  ]
  
