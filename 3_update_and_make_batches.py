import csv
import sys
import os
import re

# Run: 
# python 1_unique_label_count.py $filename $UNIQUE_LABELS_PER_CSV 
# 1st argument: $filename
# 2nd argument: $UNIQUE_LABELS_PER_CSV 
#
# make smaller batches with unique labels(column name + value) per csv

def getCSVLength(filename):
  with open(filename) as csv_object:
    return sum(1 for row in csv_object)-1 # deduct 1 for header

# User Parameter
FILENAME = sys.argv[1]
UNIQUE_LABELS_PER_CSV = int(sys.argv[2]) if len(sys.argv) > 2 else 5000

DUPLICATE_LIMITS_PER_LABEL = 2
STRING_LENGTH_LIMIT = 4
EXCEPTION_COLUMN = 'id'

# File path
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
full_path = os.path.join(CURRENT_DIR, FILENAME)
full_path_name_only = os.path.splitext(full_path)[0]

# REGEX
SPECIAL_CHAR_REGEX = '[^a-zA-Z0-9\-\_]'
ENDING_REGEX = '[-$\_$]'
REPLACE_VALUE = '-'

# Helpers
updated_rows = []
updated_rows_start_index = 0
unique_labels = {}
unique_label_index = 0
pages = []


with open(FILENAME) as infile:
  # create an object that can map with key
  reader = csv.DictReader(infile)
  header = reader.fieldnames
  CSV_LAST_INDEX = getCSVLength(FILENAME)-1
  
  for index, row in enumerate(reader):
    for column_name, column_value in row.items():
      LABEL = column_name+column_value
      if column_name != EXCEPTION_COLUMN:

        # truncate from right if the column_value length greater than limit
        column_value = column_value[:STRING_LENGTH_LIMIT] if len(
            column_value) > STRING_LENGTH_LIMIT else column_value

        # regex replace unsupported characters
        column_value = re.sub(SPECIAL_CHAR_REGEX, '-', column_value)

        # remove special characters ending
        column_value = re.sub(ENDING_REGEX, '', column_value)

        # append EXCEED_COUNT to column_value if LABEL count exceeds DUPLICATE_LIMITS_PER_LABEL
        if not LABEL in unique_labels:
          unique_labels[LABEL] = 0
        unique_labels[LABEL] += 1
        EXCEED_COUNT = int(unique_labels[LABEL]/DUPLICATE_LIMITS_PER_LABEL)
        if EXCEED_COUNT >= 1:
          column_value = column_value[:-EXCEED_COUNT] + str(EXCEED_COUNT) if len(
              column_value) == STRING_LENGTH_LIMIT else column_value + str(EXCEED_COUNT)

        # update column_value
        row[column_name] = column_value

    updated_rows.append(row)
    updated_rows_current_index = len(updated_rows)

    if(UNIQUE_LABELS_PER_CSV < len(unique_labels) or index == CSV_LAST_INDEX):
      pages.append(updated_rows[updated_rows_start_index: updated_rows_current_index])
      updated_rows_start_index = updated_rows_current_index
      unique_labels={}

for index, page in enumerate(pages):
  prefix = str(int(sys.argv[2])/1000)+'k' if int(sys.argv[2]) >= 1000 & updated_rows_start_index > 0 else str(int(sys.argv[2]))
  new_file_path='{}_{}-{}.csv'.format(full_path_name_only, prefix, str(index+1))
  with open(new_file_path, 'w+') as outfile:
    writer = csv.DictWriter(outfile, lineterminator='\n', fieldnames=header)
    writer.writeheader()
    for row in page:
      writer.writerow(row)

print('Done: splitting {} into {} files'.format(FILENAME, len(pages)))
