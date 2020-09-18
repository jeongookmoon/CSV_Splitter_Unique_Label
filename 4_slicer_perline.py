import csv
import os
import re
import argparse

parser = argparse.ArgumentParser(description='Slice based on unique labels per CSV')
parser.add_argument('-f','--filename', help='Filename', required=True)
parser.add_argument('-l','--linenumber', help='Number of lines allowed per CSV', required=True)
args = vars(parser.parse_args())

# User Parameter
FILENAME = str(args['filename'])
LINE_NUMBERS_PER_CSV = int(args['linenumber'])

# File path
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
full_path = os.path.join(CURRENT_DIR, FILENAME)
full_path_name_only = os.path.splitext(full_path)[0]

# Helpers
rows = []
pages = []
start_index = 0

with open(FILENAME) as infile:
  # create an object that can map with key
  reader = csv.DictReader(infile)
  header = reader.fieldnames
  rows = [ row for row in reader ]

  row_count = len(rows)
  while(start_index < row_count):
    pages.append(rows[start_index: start_index+LINE_NUMBERS_PER_CSV])
    start_index += LINE_NUMBERS_PER_CSV

  for index, page in enumerate(pages):
    new_file_path='{}_{}-{}.csv'.format(full_path_name_only, str(LINE_NUMBERS_PER_CSV)+'lines', str(index+1))
    with open(new_file_path, 'w+') as outfile:
      writer = csv.DictWriter(outfile, lineterminator='\n', fieldnames=header)
      writer.writeheader()
      for row in page:
        writer.writerow(row)

print('Done: splitting "{}" into "{}" files'.format(FILENAME, len(pages)))
