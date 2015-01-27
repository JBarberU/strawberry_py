sdks = [
        "iphonesimulator8.1",
        "iphoneos8.1"
       ]

class Target:
  def __init__(self, name, scheme, bundle_id):
    self.name = name
    self.scheme = scheme
    self.bundle_id = bundle_id

  def __str__(self):
    return "{ name: " + self.name + ", scheme: " + self.scheme + ", bundle_id: " + self.bundle_id + " }"


