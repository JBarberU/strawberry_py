from xc_testcase import TestCase
from result_formatter import ResultFormatterBase
from meta_line import MetaLine

class JUnitResultFormatter(ResultFormatterBase):

  file_extension = "xml"

  def format_result(self, test_cases):
    lines = ["<testsuite>\n"]

    for tc in test_cases:
      duration = 0
      err_log = ""
      for ml in tc.output:
        if ml.prefix == "Duration":
          duration = float(ml.body)
        elif ml.prefix == "Fail" or ml.prefix == "Error":
          err_log += "%s: %s" % (ml.prefix, ml.body)

     # We should be able to extract a more sensible test_name
     # but we need to think about what we do with time then... 
     # if len(tc.output) and tc.output[0].prefix == "Start":
     #   test_name = tc.output[0].body.replace("\n", "")
     # else:
     #   test_name = "unknown"

      test_name = tc.file_name

      lines.append("\t<testcase classname=\"%s\" name=\"%s\" time=\"%s\">\n" % (tc.file_name, test_name, duration))

      if not tc.result:
        if not len(tc.output):
          lines.append("\t\t<skipped />\n")
        else:
          lines.append("\t\t<failure type=\"TestFailed\">%s</failure>\n" % err_log)

      lines.append("\t</testcase>\n")

    lines.append("</testsuite>\n")

    return lines

