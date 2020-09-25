""" Split CSV based on unique labels and write them into CSVs """

import csv
import os
import re
import argparse
from common_functions import getLastIndexWithoutHeader
from common_functions import fileChecker
from common_functions import writerFiles
from common_constants import PAGES
from common_constants import HEADER

parser = argparse.ArgumentParser(description='Slice based on unique labels per CSV')
parser.add_argument('-f','--filename', type=str, help='Filename', required=True)
parser.add_argument('-u','--unique', type=int, help='Number of unique labels(column name + column value) allowed per CSV', required=True)
parser.add_argument('-e', '--exception', type=str, help='Name of exception column; This column not counted for unique labels', required=False)
args = vars(parser.parse_args())

# User Parameter
FILENAME = args['filename']
UNIQUE_LABELS_PER_CSV = args['unique']
EXCEPTION_COLUMN = args['exception'] if args['exception'] else 'year'

def sliceByUniqueLabelsAndMakePages(filename, labels_per_csv, exception_col):
  """ Splitting CSV based on unique labels and return 'pages list' & 'header' """

  # Helpers
  updated_rows = []
  updated_rows_start_index = 0
  unique_labels = {}
  unique_label_index = 0
  pages = []
  header = {}

  with open(filename) as infile:
    reader = csv.DictReader(infile)
    header = reader.fieldnames
    CSV_LAST_INDEX = getLastIndexWithoutHeader(filename)
    
    for index, row in enumerate(reader):
      for column_name, column_value in row.items():
        LABEL = column_name+column_value
        if column_name != exception_col and len(column_value) > 0:
          # print('column_name: {}, column_value: {}'.format(column_name, column_value))
          
          # handle unique labels count
          if not LABEL in unique_labels:
            unique_labels[LABEL] = 0
          unique_labels[LABEL] += 1
      
      updated_rows.append(row)
      updated_rows_current_index = len(updated_rows)
      
      # # print('index: {}, unique_labels_size: {}, CSV_LAST_INDEX: {}, Year: {}'.format(index, len(unique_labels), CSV_LAST_INDEX, row['year']))
      if(labels_per_csv < len(unique_labels) or index == CSV_LAST_INDEX):
        pages.append(updated_rows[updated_rows_start_index: updated_rows_current_index])
        updated_rows_start_index = updated_rows_current_index
        unique_labels={}
  
  print('Done: Splitting')
  return {PAGES: pages, HEADER: header}

if __name__ == '__main__':
  fileChecker(FILENAME)
  SLICED_INFO = sliceByUniqueLabelsAndMakePages(FILENAME, UNIQUE_LABELS_PER_CSV, EXCEPTION_COLUMN)
  writerFiles(SLICED_INFO[PAGES], SLICED_INFO[HEADER], FILENAME)
