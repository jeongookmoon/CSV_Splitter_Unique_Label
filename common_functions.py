import sys
import csv
import os.path

def getCSVLength(filename):
  """ Returns line numbers of CSV """
  
  with open(filename) as csv_object:
    return len(csv_object.readlines())

def getCSVLengthWithoutHeader(filename):
  """ Returns line numbers of CSV excluding header """
  
  return getCSVLength(filename)-1 # subtract 1 for header

def getLastIndexWithoutHeader(filename):
  """ Returns last index(assuming start index=0) of CSV excluding header """
  
  return getCSVLengthWithoutHeader(filename)-1 # subtract 1 since start index=0

def globChecker(file_list, filename):
  fullpath = getFullPath(filename)
  
  if len(file_list) < 1:
    sys.exit('NO file found with pattern "{}"'.format(fullpath))

def fileChecker(filename):
  """ Throws error if file not exist or if file is not CSV """
  
  fullpath = getFullPath(filename)
  
  try: 
    file = open(fullpath)

  except IOError:
    sys.exit('"{}" NOT FOUND'.format(fullpath))

  if(not filename.lower().endswith('.csv')):
    sys.exit('"{}" not supported'.format(filename))

def countLabelsLines(filename, exception_column): 
  """ Display 'filename', 'unique labels' & 'line numbers' per CSV(s) """
  
  try: 
    with open(filename) as infile:
      # Helpers
      unique_labels = {}
      
      # create an object that can map with key
      reader = csv.DictReader(infile)
      header = reader.fieldnames
      CSV_LENGTH_WITHOUT_HEADER = getCSVLengthWithoutHeader(filename)
      
      for row in reader:
        for column_name, column_value in row.items():
          LABEL = column_name+column_value
          if column_name != exception_column and len(column_value) > 0:

            if not LABEL in unique_labels:
              unique_labels[LABEL] = 0
            unique_labels[LABEL] += 1
            
    print('"{}" has "{}" unique labels and "{}" lines excluding header'.format(filename, len(unique_labels), CSV_LENGTH_WITHOUT_HEADER))
  
  except IOError:
    sys.exit('{} NOT FOUND'.format(filename))

def getFullPath(filename):
  """ Returns full path of file """
  CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
  return os.path.join(CURRENT_DIR, filename)

def getFullPathWithNameOnly(filename):
  """ Returns full path of file excluding extension """
  
  full_path = getFullPath(filename)
  return os.path.splitext(full_path)[0]
  
def writerFiles(pages, header, filename):
  """ Write CSVs('filename-1.csv, ...' where filename is) with header using pages list """
  
  FULL_PATH_NAME_ONLY = getFullPathWithNameOnly(filename)

  for index, page in enumerate(pages):
    new_file_path='{}-{}.csv'.format(FULL_PATH_NAME_ONLY, str(index+1))
    try: 
      with open(new_file_path, 'w+') as outfile:
        writer = csv.DictWriter(outfile, lineterminator='\n', fieldnames=header)
        writer.writeheader()
        for row in page:
          writer.writerow(row)
    except IOError:
      print('FAILED TO OPEN {}'.format(new_file_path))

  print('Done: Writing split pages of "{}" into "{}" files'.format(filename, len(pages)))

def writeUpdatedFile(updated_rows, header, filename):
  """ Write CSV('filename-updated.csv' at same folder where filename is) with header using updated_rows """

  FULL_PATH_NAME_ONLY = getFullPathWithNameOnly(filename)
  NEW_PATH = '{}-{}.csv'.format(FULL_PATH_NAME_ONLY, 'updated')
  try:
    with open(NEW_PATH, 'w+') as outfile:
      writer = csv.DictWriter(outfile, lineterminator='\n', fieldnames=header)
      writer.writeheader()
      for row in updated_rows:
        writer.writerow(row)
      print('Done: Writing updated file at {}'.format(NEW_PATH))

  except IOError:
    print('FAILED TO OPEN {}'.format(FULL_PATH_NAME_ONLY))
