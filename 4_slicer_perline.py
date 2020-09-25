""" Splitting CSV based on line numbers and write them into CSVs """

import csv
import os
import re
import argparse
from common_functions import fileChecker
from common_functions import writerFiles
from common_constants import PAGES
from common_constants import HEADER

parser = argparse.ArgumentParser(description='Slice based on unique labels per CSV')
parser.add_argument('-f','--filename', type=str, help='Filename', required=True)
parser.add_argument('-l','--linenumber', type=int, help='Number of lines allowed per CSV', required=True)
args = vars(parser.parse_args())

# User Parameter
FILENAME = args['filename']
LINE_NUMBERS_PER_CSV = args['linenumber']

def sliceByLinesAndMakePages(filename, lines_per_csv):
  """ Splitting CSV based on line numbers and return 'pages list' & 'header' """

  # Helpers
  rows = []
  pages = []
  start_index = 0

  with open(filename) as infile:
    reader = csv.DictReader(infile)
    header = reader.fieldnames
    rows = [ row for row in reader ]

    row_count = len(rows)
    while(start_index < row_count):
      pages.append(rows[start_index: start_index+lines_per_csv])
      start_index += LINE_NUMBERS_PER_CSV
  
  print('Done: Splitting')
  return {PAGES: pages, HEADER: header}

if __name__ == '__main__':
  fileChecker(FILENAME)
  SLICED_INFO = sliceByLinesAndMakePages(FILENAME, LINE_NUMBERS_PER_CSV)
  writerFiles(SLICED_INFO[PAGES], SLICED_INFO[HEADER], FILENAME)
