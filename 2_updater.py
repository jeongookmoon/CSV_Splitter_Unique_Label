""" 
Updates followings and write to a new file
1. Any character other than 'lower/uppercase alphabet, number, - and _ characters' get replaced by '-'
2. '-' or '_' get removed recursively if they exist at start or end
3. Label('column_name'+'column_value') length get right-striped to match max string value (Default: 20)
4. Column value gets new postfix(1,2,3...) if more than items(exception column) cap in a label (Default: 1000)
"""

import csv
import os
import re
import argparse
from common_functions import writeUpdatedFile
from common_functions import fileChecker
from common_constants import ROWS
from common_constants import HEADER

parser = argparse.ArgumentParser(description='Update CSV')
parser.add_argument('-f','--filename', type=str, help='Filename', required=True)
parser.add_argument('-c','--cap', type=int, help='Items(which is under exception column) cap per label (header+column_value)', required=False)
parser.add_argument('-m','--maxstring', type=int, help='Max length allowed for column value', required=False)
parser.add_argument('-e', '--exception', type=str, help='Name of exception column; This column not counted for unique labels', required=False)
args = vars(parser.parse_args())

# User Parameter
FILENAME = args['filename']
CAP_PER_LABEL = args['cap']-1 if args['cap'] else 999 # deduct 1 since index start = 0
STRING_LENGTH_LIMIT = args['maxstring'] if args['maxstring'] else 20
EXCEPTION_COLUMN = args['exception'] if args['exception'] else 'spec'

# REGEX
SPECIAL_CHAR_REGEX = re.compile(r'[^a-zA-Z0-9-_]')

def findNewLabel(column_name, column_value, defcount_limit, string_length, unique_labels):
  """ Find new label that has less unique exception column values than defcount limit by adding/putting postfix (1, 2, 3 ...) in the last character """

  postfix=0
  new_label=str(column_name)+str(column_value)
  new_column_value=column_value
 
  while(new_label in unique_labels and unique_labels[new_label]>defcount_limit):
    postfix+=1
    new_column_value = column_value[:-len(str(postfix))]+str(postfix) if len(column_value+str(postfix)) > string_length else column_value+str(postfix)
    new_label=column_name+new_column_value

  return new_label, new_column_value

def trimmer(label):
  """ Remove - or _ at start or end """

  while(label.startswith('-') or label.startswith('_') or label.endswith('-') or label.endswith('_')):
    label = label.lstrip('-').lstrip('_').rstrip('-').rstrip('_')

  return label

def updater(filename, cap_per_label, label_length_limit, exception_col):
  """ 
  Updates followings and return updated rows & header
  1. Any character other than 'lower/uppercase alphabet, number, - and _ characters' get replaced by '-'
  2. '-' or '_' get removed recursively if they exist at start or end
  3. Label('column_name'+'column_value') length get right-striped to match max string value (Default: 20)
  4. Column value gets new postfix(1,2,3...) if more than items(exception column) cap in a label (Default: 1000)
  """
  
  # Helpers
  updated_rows = []
  updated_rows_start_index = 0
  unique_labels = {}
  unique_label_index = 0
  REPLACE_VALUE = '-'

  with open(filename) as infile:
    # create an object that can map with key
    reader = csv.DictReader(infile)
    header = reader.fieldnames
    
    for index, row in enumerate(reader):
      for column_name, column_value in row.items():
        label_value = column_name+column_value
        
        if column_name != exception_col and len(column_value) > 0:
          new_column_length = label_length_limit-len(column_name)-1 # subtract 1 for "="

          # truncate from right if the column_value length greater than limit
          column_value = column_value[:new_column_length] if len(
              column_value) > new_column_length else column_value

          # regex replace unsupported characters
          column_value = re.sub(SPECIAL_CHAR_REGEX, REPLACE_VALUE, column_value)

          # remove special characters at beginning and ending recursively
          column_value = trimmer(column_value)

          # find new label, column value
          label_value, column_value = findNewLabel(column_name, column_value, cap_per_label, new_column_length, unique_labels)

          if not label_value in unique_labels:
            unique_labels[label_value] = 0
          unique_labels[label_value] += 1
          
          # update column_value
          row[column_name] = column_value

      updated_rows.append(row)
      updated_rows_current_index = len(updated_rows)
  
  
    print('Done: Updating Rows')
    return {ROWS: updated_rows, HEADER: header}

if __name__ == '__main__':
  fileChecker(FILENAME)
  UPDATED_INFO = updater(FILENAME, CAP_PER_LABEL, STRING_LENGTH_LIMIT, EXCEPTION_COLUMN)
  writeUpdatedFile(UPDATED_INFO[ROWS], UPDATED_INFO[HEADER], FILENAME)
