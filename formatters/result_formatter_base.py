from log import Log

class ResultFormatterBase:

  file_extension = None

  def format_result(self, test_cases):
    Log.err("BaseFormatter doesn't know what to do :(")


