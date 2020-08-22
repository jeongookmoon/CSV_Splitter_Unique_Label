import csv
import sys
import os
import re

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
filename = sys.argv[1]
prefix = sys.argv[3]

full_file_path = os.path.join(CURRENT_DIR, filename)
file_name = os.path.splitext(full_file_path)[0]

rows_per_csv = int(sys.argv[2]) if len(sys.argv) > 2 else 5000
definition = 'id'

updated_rows = []
LENGTH_LIMIT = 4
SPECIAL_CHAR_REGEX = '[^a-zA-Z0-9\-\_]'
ENDING_REGEX = '[-$\_$]'
REPLACE_VALUE = '-'

unique_label_counter = {}
LABEL_DUP_LIMIT = 2

with open(filename) as infile:
    # create an object that can map with key
    reader = csv.DictReader(infile)
    header = reader.fieldnames

    for row in reader:
      for key, value in row.items():
        LABEL = key+value
        if key != definition:
          # truncate from right if the value length greater than limit
          value = value[:LENGTH_LIMIT] if len(value) > LENGTH_LIMIT else value 
          # regex replace unsupported characters
          value = re.sub(SPECIAL_CHAR_REGEX, '-', value)
          # remove special characters ending
          value = re.sub(ENDING_REGEX, '', value)
          # add number on value for the label counter exceed label limit
          if not LABEL in unique_label_counter:
            unique_label_counter[LABEL] = 0
          unique_label_counter[LABEL] += 1
          EXCEED_COUNT = int(unique_label_counter[LABEL]/LABEL_DUP_LIMIT)
          if EXCEED_COUNT >= 1:
            value = value[:-1] + str(EXCEED_COUNT) if len(value) == LENGTH_LIMIT else value + str(EXCEED_COUNT)
          row[key] = value
      updated_rows.append(row)

    
    print('%s' % ', '.join(map(str, updated_rows)))
    