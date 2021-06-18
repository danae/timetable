import argparse
import sys
import timetable


# Main function
def main(args):
  # Parse the arguments
  parser = argparse.ArgumentParser(prog = args[0], description = "Parse a GATT timetable")
  parser.add_argument('file', help = "timetable file to parse")
  args = parser.parse_args(args[1:])

  # Parse the timetable files
  feed = timetable.load_feed(args.file)
  print(feed.report())


# Execute the main function
if __name__ == "__main__":
  main(sys.argv)
