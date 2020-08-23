import argparse
from glob import glob
from common_functions import fileChecker
from common_functions import countLabelsLines

parser = argparse.ArgumentParser(description='Counts unique labels and number of lines in CSV(s)')
parser.add_argument('-f','--filename', help='Filename; if * is included, it will find all files matching the pattern')
parser.add_argument('-e', '--exception', help='Name of exception column; This column not counted for unique labels', required=False)
args = vars(parser.parse_args())

# User Parameter
FILENAME = glob(args['filename']) if '*' in args['filename'] else args['filename']
EXCEPTION_COLUMN = args['exception'] if args['exception'] else 'spec'

if isinstance(FILENAME, str):
  if (fileChecker(FILENAME)):
    countLabelsLines(FILENAME, EXCEPTION_COLUMN)
else:
  for eachfile in FILENAME:
    if (fileChecker(eachfile)):
      countLabelsLines(eachfile, EXCEPTION_COLUMN)
