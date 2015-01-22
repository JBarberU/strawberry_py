class BuildFormatterBase():

  def __init__(self):
    self.pipe = None

  def start(self, pipe):
    self.pipe = pipe

  def stop(self, return_code):
    pass

  def save(self):
    pass


