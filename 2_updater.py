import csv
import os
import re
import argparse

parser = argparse.ArgumentParser(description='Update CSV')
parser.add_argument('-f','--filename', help='Filename', required=True)
parser.add_argument('-d','--duplicate', help='Number of duplicate allowance for each label', required=False)
parser.add_argument('-m','--maxstring', help='Max length allowed for column value', required=False)
parser.add_argument('-e', '--exception', help='Name of exception column; This column not counted for unique labels', required=False)
args = vars(parser.parse_args())

# User Parameter
FILENAME = str(args['filename'])
DUPLICATE_LIMITS_PER_LABEL = int(args['duplicate']) if args['duplicate'] else 5000
STRING_LENGTH_LIMIT = int(args['maxstring']) if args['maxstring'] else 63
EXCEPTION_COLUMN = str(args['exception']) if args['exception'] else 'spec'

# File path
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
full_path = os.path.join(CURRENT_DIR, FILENAME)
full_path_name_only = os.path.splitext(full_path)[0]

# REGEX
SPECIAL_CHAR_REGEX = '[^a-zA-Z0-9-_]'
REPLACE_VALUE = '-'

# Helpers
updated_rows = []
updated_rows_start_index = 0
unique_labels = {}
unique_label_index = 0
SPLITTER = '-'

def findNewLabel(column_name, column_value, duplicate_limit, string_length):
  postfix=0
  new_label=str(column_name)+str(column_value)
  new_column_value=column_value
  while(new_label in unique_labels and unique_labels[new_label]>duplicate_limit):
    postfix+=1
    new_column_value = column_value[:-len(str(postfix))]+str(postfix) if len(column_value+str(postfix)) > string_length else column_value+str(postfix)
    new_label=column_name+new_column_value
  return new_label, new_column_value
  
with open(FILENAME) as infile:
  # create an object that can map with key
  reader = csv.DictReader(infile)
  header = reader.fieldnames
  
  for index, row in enumerate(reader):
    for column_name, column_value in row.items():
      label_value = column_name+column_value
      if column_name != EXCEPTION_COLUMN and len(column_value) > 0:

        # truncate from right if the column_value length greater than limit
        column_value = column_value[:STRING_LENGTH_LIMIT] if len(
            column_value) > STRING_LENGTH_LIMIT else column_value

        # regex replace unsupported characters
        column_value = re.sub(SPECIAL_CHAR_REGEX, '-', column_value)

        # remove special characters at beginning and ending
        column_value = column_value.lstrip('-').lstrip('_').rstrip('-').rstrip('_')

        # find new label and column value that match string length limit and duplicate label limit
        label_value, column_value = findNewLabel(column_name, column_value, DUPLICATE_LIMITS_PER_LABEL, STRING_LENGTH_LIMIT)

        if not label_value in unique_labels:
          unique_labels[label_value] = 0
        unique_labels[label_value] += 1
        
        # update column_value
        row[column_name] = column_value

    updated_rows.append(row)
    updated_rows_current_index = len(updated_rows)

with open('{}-{}.csv'.format(full_path_name_only, 'updated'), 'w+') as outfile:
  writer = csv.DictWriter(outfile, lineterminator='\n', fieldnames=header)
  writer.writeheader()
  for row in updated_rows:
    writer.writerow(row)

print('Done: Updating "{}"'.format(FILENAME))

