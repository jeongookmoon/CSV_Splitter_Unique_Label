import csv
import os
import re
import argparse

parser = argparse.ArgumentParser(description='Slice based on unique labels per CSV')
parser.add_argument('-f','--filename', help='Filename', required=True)
parser.add_argument('-u','--unique', help='Number of unique labels(column name + column value) allowed per CSV', required=True)
parser.add_argument('-e', '--exception', help='Name of exception column; This column not counted for unique labels', required=False)
args = vars(parser.parse_args())

# User Parameter
FILENAME = str(args['filename'])
UNIQUE_LABELS_PER_CSV = int(args['unique'])
EXCEPTION_COLUMN = str(args['exception']) if args['exception'] else 'spec'

# File path
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
full_path = os.path.join(CURRENT_DIR, FILENAME)
full_path_name_only = os.path.splitext(full_path)[0]

# Helpers
updated_rows = []
updated_rows_start_index = 0
unique_labels = {}
unique_label_index = 0
pages = []

def getCSVLength(filename):
  with open(filename) as csv_object:
    return sum(1 for row in csv_object)-1 # deduct 1 for header

with open(FILENAME) as infile:
  # create an object that can map with key
  reader = csv.DictReader(infile)
  header = reader.fieldnames
  CSV_LAST_INDEX = getCSVLength(FILENAME)-1
  
  for index, row in enumerate(reader):
    for column_name, column_value in row.items():
      LABEL = column_name+column_value
      if column_name != EXCEPTION_COLUMN:
        if not LABEL in unique_labels:
          unique_labels[LABEL] = 0
        unique_labels[LABEL] += 1
    
    updated_rows.append(row)
    updated_rows_current_index = len(updated_rows)
    
    if(UNIQUE_LABELS_PER_CSV < len(unique_labels) or index == CSV_LAST_INDEX):
      pages.append(updated_rows[updated_rows_start_index: updated_rows_current_index])
      updated_rows_start_index = updated_rows_current_index
      unique_labels={}

for index, page in enumerate(pages):
  new_file_path='{}_{}-{}.csv'.format(full_path_name_only, str(UNIQUE_LABELS_PER_CSV), str(index+1))
  with open(new_file_path, 'w+') as outfile:
    writer = csv.DictWriter(outfile, lineterminator='\n', fieldnames=header)
    writer.writeheader()
    for row in page:
      writer.writerow(row)

print('Done: splitting "{}" into "{}" files'.format(FILENAME, len(pages)))
