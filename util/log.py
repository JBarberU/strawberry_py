from colors import Colors

class Log:

  @classmethod
  def print_msg(cls, title, msg, color):
    print("%s%s%s: %s" % (color, title, Colors.NORMAL, msg))

  @classmethod
  def msg(cls, msg_in):
    Log.print_msg("Message", msg_in, Colors.GREEN)

  @classmethod
  def info(cls, msg_in):
    Log.print_msg("Info", msg_in, Colors.BLUE)

  @classmethod
  def warn(cls, msg_in):
    Log.print_msg("Warning", msg_in, Colors.YELLOW)

  @classmethod
  def err(cls, msg_in):
    Log.print_msg("Error", msg_in, Colors.RED)
