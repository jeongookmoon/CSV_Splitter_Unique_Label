## Smaller Batch Maker based on Unique Labels Count Per CSV
![](counter_updater_slicer.gif)
* Slicer moves to next file once unique label count goes beyond the limit per CSV

## Help
"-h" gives usage info. Example:
```
python .\1_counter.py -h
usage: 1_counter.py [-h] -f FILENAME [-e EXCEPTION]

Counts unique labels and number of lines in CSV(s)

optional arguments:
  -h, --help            show this help message and exit
  -f FILENAME, --filename FILENAME
                        Filename; if * is included, it will find all files matching the pattern
  -e EXCEPTION, --exception EXCEPTION
                        Name of exception column; This column not counted for unique labels
```

## 1. Counter
Counts how many unique labels (column name+value) and lines excluding header in CSV.
Can take both singular string or string with asterisk to find all files matching the pattern.
```
python .\1_counter.py -f .\annual-enterprise-survey-2019-financial-year-provisional-size-bands.csv -e year
".\annual-enterprise-survey-2019-financial-year-provisional-size-bands.csv" has "6376" unique labels and "13932" lines excluding header

python .\1_counter.py -f .\annual-enterprise-survey-2019-financial-year-provisional-size-bands_1.5k-* -e year
".\annual-enterprise-survey-2019-financial-year-provisional-size-bands_1.5k-1.csv" has "1501" unique labels and "1973" lines excluding header
".\annual-enterprise-survey-2019-financial-year-provisional-size-bands_1.5k-2.csv" has "1501" unique labels and "1881" lines excluding header
".\annual-enterprise-survey-2019-financial-year-provisional-size-bands_1.5k-3.csv" has "1501" unique labels and "1930" lines excluding header
".\annual-enterprise-survey-2019-financial-year-provisional-size-bands_1.5k-4.csv" has "1501" unique labels and "1944" lines excluding header
".\annual-enterprise-survey-2019-financial-year-provisional-size-bands_1.5k-5.csv" has "1501" unique labels and "1904" lines excluding header
".\annual-enterprise-survey-2019-financial-year-provisional-size-bands_1.5k-6.csv" has "1501" unique labels and "1793" lines excluding header
".\annual-enterprise-survey-2019-financial-year-provisional-size-bands_1.5k-7.csv" has "1501" unique labels and "1816" lines excluding header
".\annual-enterprise-survey-2019-financial-year-provisional-size-bands_1.5k-8.csv" has "649" unique labels and "691" lines excluding header
```

## 2. Updater
1. Truncate excess length of column value
2. Replace unsupported characters with '-'
3. Remove special characters at the start or end recursively
4. Replace with the new label (Find recursively by adding postfix number to avoid duplicate allowance per label limit) 

Example: Update CSV with allowing ten different years per label, max string for column value = 60, exception column = year
```
python .\2_updater.py -f .\annual-enterprise-survey-2019-financial-year-provisional-size-bands.csv -d 10 -m 60 -e year
Done: Updating ".\annual-enterprise-survey-2019-financial-year-provisional-size-bands.csv"
```

## 3. Slicer by Unique Label Count per CSV
Slice the CSV into smaller files based on allowed unique labels count per CSV

Example: Slice CSV into smaller CSVs of 1500 unique labels with exception column = year
```
python .\3_slicer.py -f .\annual-enterprise-survey-2019-financial-year-provisional-size-bands.csv -u 1500 -e year
Done: splitting ".\annual-enterprise-survey-2019-financial-year-provisional-size-bands.csv" into "8" files
```

## 4. Slicer by Number of Lines per CSV
Slice the CSV into smaller files based on number of lines per CSV

Example: Slice CSV into smaller CSVs of 5000 lines each
```
python .\4_slicer_perline.py -f .\annual-enterprise-survey-2019-financial-year-provisional-size-bands.csv -l 5000
Done: splitting ".\annual-enterprise-survey-2019-financial-year-provisional-size-bands.csv" into "3" files
```

Example CSV from
https://www.stats.govt.nz/large-datasets/csv-files-for-download/
```