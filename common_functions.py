import csv
import os.path

def getCSVLength(filename):
  with open(filename) as csv_object:
    return sum(1 for row in csv_object)

def fileChecker(filename):
  return os.path.isfile(filename)

def countLabelsLines(filename, exception_column):
  with open(filename) as infile:
    # Helpers
    unique_labels = {}
    # create an object that can map with key
    reader = csv.DictReader(infile)
    header = reader.fieldnames
    CSV_LAST_INDEX = getCSVLength(filename)-1
    for row in reader:
      for column_name, column_value in row.items():
        LABEL = column_name+column_value
        if column_name != exception_column:
          if not LABEL in unique_labels:
            unique_labels[LABEL] = 0
          unique_labels[LABEL] += 1
  print('"{}" has "{}" unique labels and "{}" lines excluding header'.format(filename, len(unique_labels), CSV_LAST_INDEX))
