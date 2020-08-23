import csv
import sys

# Run: 
# python 1_unique_label_count.py $filename
#
# returns # of unique label(column name + value)

# User Parameter
FILENAME = sys.argv[1]

# Helpers
unique_labels = {}

with open(FILENAME) as infile:
  # create an object that can map with key
  reader = csv.DictReader(infile)
  header = reader.fieldnames

  for row in reader:
    for column_name, column_value in row.items():
      LABEL = column_name+column_value
      if column_name != EXCEPTION_COLUMN:
        if not LABEL in unique_labels:
          unique_labels[LABEL] = 0
        unique_labels[LABEL] += 1

  print('{} has {} unique labels'.format(FILENAME, len(unique_labels)))

