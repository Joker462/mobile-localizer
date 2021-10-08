# mobile-localizer
This command tool writing in Python. It allows iOS and Android developers to save time doing the manual copy and paste in their localizable string list.

Thank [Roger Molas](https://github.com/rogermolas/csv-localizer) author for writing convert csv file to localizable string list. I only write a script to convert localizable string list to CSV file.

## Requirements
#### CSV File in this format:
| key| en| vi |
| :------|:-------------:|:-------------:|

Sample CSV

| key| en| vi |
| :------|:-------------:|:-------------:|
|pause_key |paused | dừng |
|start_key |start| bắt đầu |
|stop_key | stop |kết thúc |

## Installation
- Requires Python 3.0 or above.

- Just only clone this source and using the command to direct at the root of this source in terminal or cmd.

- Need to install [openpyxl](https://openpyxl.readthedocs.io) for using xlsx files.

## Usage
```
Commands:
  make android2csv     # Convert .xml files to CSV file (need to copy all values folders into Input directory)
  make csv2android     # Convert CSV file to .xml (need to copy csv file into Input directory)
  make xlsx2android    # Convert XLSX file to .xml (need to copy xlsx file into Input directory)
  make ios2csv         # Convert .strings file to CSV file (need to copy all .Iproj folders into Input directory)
  make csv2ios         # Convert CSV file to .strings (need to copy csv file into Input directory)
  make xlsx2ios        # Convert XLSX file to .strings (need to copy csv file into Input directory)
  make xlsx2json       # Convert XLSX file to JSON file (need to copy xlsx file into Input directory)
  make csv2json        # Convert CSV file to JSON file (need to copy csv file into Input directory)
```

## License

The MIT License (MIT)

Copyright (c) 2020 Hung Thai (hungthai270893@gmail.com)
