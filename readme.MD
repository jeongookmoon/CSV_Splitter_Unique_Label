# 4 CSV Tools: Counter, Updater and 2 Splitter 
1. Counter: counts unique labels(column name+value) and line numbers
2. Updater: replace unsupported chars, adjust length, get new name with postfix, strip start and end char if special char
3. Splitter per Unique Labels: Split CSV based on unique labels(column name+value)
4. Splitter per Line Numbers: Split CSV based on number of lines 

![](counter_updater_slicer.gif)

## Help/Usage
"-h" gives usage info. 

### Example:
```
$python .\1_counter.py -h
usage: 1_counter.py [-h] -f FILENAME [-e EXCEPTION]

Counts unique label and number of lines in CSV(s)

optional arguments:
  -h, --help            show this help message and exit
  -f FILENAME, --filename FILENAME
                        Filename; if * is included, it will find all files matching the pattern
  -e EXCEPTION, --exception EXCEPTION
                        Name of exception column; This column not counted for unique label(column name+value)
```

## 1. Counter
Display 'filename', 'unique labels(column name+value)' & 'line numbers' per CSV(s), and total "line numbers" for CSVs

### Example of single CSV:
```
$ python .\1_counter.py -f .\annual-enterprise-survey-2019-financial-year-provisional-size-bands.csv -e year
".\annual-enterprise-survey-2019-financial-year-provisional-size-bands.csv" has "6376" unique labels and "13932" lines excluding header
```

### Example of multiple CSVs:
```
$ python .\1_counter.py -f .\annual-enterprise-survey-2019-financial-year-provisional-size-bands-updated-* -e year
".\annual-enterprise-survey-2019-financial-year-provisional-size-bands-updated-1.csv" has "3001" unique labels and "3615" lines excluding header
".\annual-enterprise-survey-2019-financial-year-provisional-size-bands-updated-2.csv" has "3001" unique labels and "3571" lines excluding header
".\annual-enterprise-survey-2019-financial-year-provisional-size-bands-updated-3.csv" has "3001" unique labels and "3588" lines excluding header
".\annual-enterprise-survey-2019-financial-year-provisional-size-bands-updated-4.csv" has "2870" unique labels and "3158" lines excluding header
Total lines: 13932
```

### Parameters
-f (filename, **required**)
-e (exception column, optional: default="year")

### Skipping optional fields achieve the same. 
```
$ python .\1_counter.py -f .\annual-enterprise-survey-2019-financial-year-provisional-size-bands.csv
".\annual-enterprise-survey-2019-financial-year-provisional-size-bands.csv" has "6376" unique labels and "13932" lines excluding header
```

### Using non 'year' exception -> uses all columns for unique label count
```
$ python .\1_counter.py -f .\annual-enterprise-survey-2019-financial-year-provisional-size-bands.csv -e somethingelse
".\annual-enterprise-survey-2019-financial-year-provisional-size-bands.csv" has "6385" unique labels and "13932" lines excluding header
```

## 2. Updater
Write a updated(Replace unsupported chars with '-', remove special char at start&end, adjust label length, put post fix if items(exception column) cap per label exceeds) CSV.

### Updates following items:
1. Any character other than 'lower/uppercase alphabet, number, - and _ characters' get replaced by '-'
2. '-' or '_' get removed recursively if they exist at start or end
3. Label('column_name'+'column_value') length get right-striped to match max string value (Default: 63)
4. Column value gets new postfix(1,2,3...) if more than items(exception column) cap per label (Default: 5000)

### Example:
```
$ python .\2_updater.py -f .\annual-enterprise-survey-2019-financial-year-provisional-size-bands.csv -c 30 -m 50 -e year
Done: Updating Rows
Done: Writing updated file at C:\Projects\Python_CSV_Update_Make_Batches_Per_Label_Counts\.\annual-enterprise-survey-2019-financial-year-provisional-size-bands-updated.csv
```

### Parameters:
-f (filename, **required**)
-c (items cap per label, optional:default=1000)
-m (label character length limit, optional:default=20)
-e (exception column, optional: default="year")

### Unique labels increase after update (due to new labels; column name + new column value):
```
Original File:
$ python .\1_counter.py -f .\annual-enterprise-survey-2019-financial-year-provisional-size-bands.csv -e year
".\annual-enterprise-survey-2019-financial-year-provisional-size-bands.csv" has "6376" unique labels and "13932" lines excluding header

Updated File:
$ python .\1_counter.py -f .\annual-enterprise-survey-2019-financial-year-provisional-size-bands-updated.csv -e year
".\annual-enterprise-survey-2019-financial-year-provisional-size-bands-updated.csv" has "8671" unique labels and "13932" lines excluding header
```

## 3. Slicer per unique labels
Split CSV based on unique labels and write them into CSVs

### Example:
```
$ python .\3_slicer_perlabel.py -f .\annual-enterprise-survey-2019-financial-year-provisional-size-bands-updated.csv -u 3000 -e year
Done: Splitting
Done: Writing split pages of ".\annual-enterprise-survey-2019-financial-year-provisional-size-bands-updated.csv" into "4" files
```

### Parameters:
-f (filename, **required**)
-u (number of unique labels per CSV, **required**)
-e (exception column, optional: default="year")

### Validation:
```
$ python .\1_counter.py -f .\annual-enterprise-survey-2019-financial-year-provisional-size-bands-updated-* -e year
".\annual-enterprise-survey-2019-financial-year-provisional-size-bands-updated-1.csv" has "3001" unique labels and "3615" lines excluding header
".\annual-enterprise-survey-2019-financial-year-provisional-size-bands-updated-2.csv" has "3001" unique labels and "3571" lines excluding header
".\annual-enterprise-survey-2019-financial-year-provisional-size-bands-updated-3.csv" has "3001" unique labels and "3588" lines excluding header
".\annual-enterprise-survey-2019-financial-year-provisional-size-bands-updated-4.csv" has "2870" unique labels and "3158" lines excluding header
Total lines: 13932
```

## 4. Slicer per number of lines
Split CSV based on number of lines and write them into CSVs

### Example:
```
$ python .\4_slicer_perline.py -f .\annual-enterprise-survey-2019-financial-year-provisional-size-bands-updated.csv -l 5000
Done: Splitting
Done: Writing split pages of ".\annual-enterprise-survey-2019-financial-year-provisional-size-bands-updated.csv" into "3" files
```

### Parameters:
-f (filename, **required**)
-l (number of lines per CSV, **required**)

### Validation:
```
$ python .\1_counter.py -f .\annual-enterprise-survey-2019-financial-year-provisional-size-bands-updated-* -e year
".\annual-enterprise-survey-2019-financial-year-provisional-size-bands-updated-1.csv" has "3847" unique labels and "5000" lines excluding header
".\annual-enterprise-survey-2019-financial-year-provisional-size-bands-updated-2.csv" has "3983" unique labels and "5000" lines excluding header
".\annual-enterprise-survey-2019-financial-year-provisional-size-bands-updated-3.csv" has "3356" unique labels and "3932" lines excluding header
Total lines: 13932
```
