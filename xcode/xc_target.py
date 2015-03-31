sdks = [
        "iphonesimulator8.1",
        "iphoneos8.1",
        "iphonesimulator8.2",
        "iphoneos8.2"
       ]

class Target:
  def __init__(self,
               name,
               scheme,
               app_name,
               configuration,
               bundle_id,
               provisioning_profile,
               codesigning_identity):
    self.name = name
    self.scheme = scheme
    self.app_name = app_name
    self.configuration = configuration
    self.bundle_id = bundle_id
    self.provisioning_profile = provisioning_profile
    self.codesigning_identity = codesigning_identity

  def __str__(self):
    return "{ name: {0}, scheme: {1}, bundle_id: {2}, provisioning_profile: {3}, codesigning_identity: {4} }".format(self.name, self.scheme, self.bundle_id, self.provisioning_profile, self.codesigning_identity)

  @classmethod
  def serialize(cls, targets = []):
    json_list = []
    for tgt in targets:
      json_list.append({
        "name": tgt.name,
        "scheme": tgt.scheme,
        "app_name": tgt.app_name,
        "configuration": tgt.configuration,
        "bundle_id": tgt.bundle_id,
        "codesigning_identity": tgt.codesigning_identity,
        "provisioning_profile": tgt.provisioning_profile
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
        bundle_id=tgt["bundle_id"],
        provisioning_profile=tgt["provisioning_profile"],
        codesigning_identity=tgt["codesigning_identity"]
      ))
    return target_list


