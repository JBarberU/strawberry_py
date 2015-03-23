sdks = [
        "iphonesimulator8.1",
        "iphoneos8.1",
        "iphonesimulator8.2",
        "iphoneos8.2"
       ]

class Target:
  def __init__(self, name, scheme, app_name, configuration, bundle_id):
    self.name = name
    self.scheme = scheme
    self.app_name = app_name
    self.configuration = configuration
    self.bundle_id = bundle_id

  def __str__(self):
    return "{ name: " + self.name + ", scheme: " + self.scheme + ", bundle_id: " + self.bundle_id + " }"

  @classmethod
  def serialize(cls, targets = []):
    json_list = []
    for tgt in targets:
      json_list.append({
        "name": tgt.name,
        "scheme": tgt.scheme,
        "app_name": tgt.app_name,
        "configuration": tgt.configuration,
        "bundle_id": tgt.bundle_id
      })
    return json_list

  @classmethod
  def deserialize(cls, json_targets = []):
    target_list = []
    for tgt in json_targets:
      target_list.append(Target(
        name=tgt["name"],
        scheme=tgt["scheme"],
        app_name=tgt["app_name"],
        configuration=tgt["configuration"],
        bundle_id=tgt["bundle_id"]
      ))
    return target_list


