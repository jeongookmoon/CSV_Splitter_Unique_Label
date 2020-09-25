""" Run counter to display 'filename', 'unique label(column name+value)' & 'line numbers' per CSV(s), and total "line numbers" for CSVs"""

import argparse
from glob import glob
from common_functions import fileChecker
from common_functions import globChecker
from common_functions import countLabelsLines
from common_functions import getCSVLengthWithoutHeader

parser = argparse.ArgumentParser(description='Counts unique label and number of lines in CSV(s)')
parser.add_argument('-f','--filename', type=str, help='Filename; if * is included, it will find all files matching the pattern', required=True )
parser.add_argument('-e', '--exception', type=str, help='Name of exception column; This column not counted for unique label(column name+value)', required=False)
args = vars(parser.parse_args())

# User Parameter
FILE_ARGUMENT = args['filename']
FILE_LIST = glob(FILE_ARGUMENT)
EXCEPTION_COLUMN = args['exception'] if args['exception'] else 'year'

# Check glob
globChecker(FILE_LIST, FILE_ARGUMENT)

def counter(filelist, exception_col):
  """ Display 'filename', 'unique label(column name+value)' & 'line numbers' per CSV(s), and total "line numbers" for CSVs """
  count = 0
  
  for eachfile in filelist:
      fileChecker(eachfile)
      countLabelsLines(eachfile, exception_col)
      count+=getCSVLengthWithoutHeader(eachfile)

  if count > 0 and len(filelist) > 1:
      print('Total lines: {}'.format(count))

if __name__ == '__main__':
  counter(FILE_LIST, EXCEPTION_COLUMN)