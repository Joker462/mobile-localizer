#!/usr/bin/env python
import sys, argparse, logging, os, re
from openpyxl import Workbook

IN_PATH = None
OUT_PATH = None
PLATFORM = None

# Gather our code in a main() function
def main(args, loglevel):
    logging.basicConfig(format="%(message)s", level=loglevel)
    IN_PATH = args.input
    OUT_PATH = args.output
    PLATFORM = args.platform
    print '\n'
    logging.info("Start generate xlsx file .... ")
    print '\n'
    logging.info("------------------------------------")
    
    # check source path
    logging.debug("\n")
    logging.debug("Validating source path ...")
    logging.debug("\n")
    if not os.path.exists(IN_PATH):
      logging.error('Source path not found, Invalid path.')
      logging.debug("\n")
      return
    logging.debug("Valid source path, finding {0} localization directories ...".format(PLATFORM))
    logging.debug("\n")
    logging.debug("Validating target path ...")
    logging.debug("\n")
    # check output path
    if not os.path.exists(OUT_PATH):
      logging.error('Target path not found, Invalid path.')
      logging.debug("\n")
      return
    logging.debug("Valid target path, generating output directory ...")
    logging.debug("\n")
    
    # generate output directory
    OUTPUT_DIR = os.path.join(OUT_PATH, "Output/{0}".format(PLATFORM))
    if not os.path.exists(OUTPUT_DIR):
      os.makedirs(OUTPUT_DIR)
      logging.debug("Output directory generated : %s" % OUTPUT_DIR)
      logging.debug("\n")
    else:
      logging.debug("Using output directory: %s" % OUTPUT_DIR)
      logging.debug("\n")

    logging.info("Generated output directory: %s" % OUTPUT_DIR)
    # check platform
    logging.debug("\n")
    if PLATFORM == "ios":
      logging.debug("Platform : %s" % PLATFORM)
      generate_xlsx_from_ios(IN_PATH, OUTPUT_DIR)
    elif PLATFORM == "android":
      logging.debug("Platform : %s" % PLATFORM)
      generate_xlsx_from_android(IN_PATH, OUTPUT_DIR)
    else:
      logging.warn("Invalid platform, platform should be ios, android.")
      logging.debug("\n")
      logging.error('ERROR GENERATING.\n')
      return

    print '\n'
    logging.info("DONE GENERATING.\n")
    
    
# =========================================================================
# ++++++++++++++++++++++++++++ Translation ++++++++++++++++++++++++++++++++
# =========================================================================
class Translation:
    def __init__(self, key, values):
        self.key = key
        self.values = values


def find_translation(translation_list, key):
    for transObject in translation_list:
        if transObject.key == key:
            return transObject
    return False
    
# =========================================================================
# ++++++++++++++++++++++ Generate xlsx file from iOS +++++++++++++++++++++++
# =========================================================================
def generate_xlsx_from_ios(source_path, out_path):
    endswithFolder = ".lproj"
    fields = ["key"]
    rows = []
    translationList = []
    originFilePaths = []
    full_out_paths = None

    for paths, roots, filenames in os.walk(source_path):
        if (paths.endswith(endswithFolder)):
            originFilePath = os.path.join(paths, "Localizable.strings")
            originFilePaths.append(originFilePath)
            
    originFilePaths.sort()
    
    for originFilePath in originFilePaths:
        arrRootPath = originFilePath.split("/")
        dirname = arrRootPath[len(arrRootPath) - 2]
        fields.append(dirname.replace(endswithFolder, ""))
        multiline_comment_flag = False
        tempCol = []
        with open(originFilePath, "r") as f:
            for line in f:
                if not multiline_comment_flag:
                    if line.startswith('/*') and not line[:-1].endswith('*/'):
                        multiline_comment_flag = True
                        if line[:-1].endswith('*/'):
                            multiline_comment_flag = False
                        continue
                    else:
                        line = line.split('#')[0]
                        # Empty line
                        if line == "\n":
                            continue
                        # Comment line
                        elif line and line.startswith('/*'):
                            # Check translation key exist in translation list
                            if any(x.key == line.strip() for x in translationList):
                                continue
                            else:
                                translationList.append(Translation(line.strip(), [True]))
                        elif line:
                            lineSearch = re.search('\"(.*)\"\\s*\=\\s*\"(.*)\"\;', line.strip())
                            if lineSearch:
                                tempKey = lineSearch.group(1)
                                tempVal = lineSearch.group(2)
                                transObject = find_translation(translationList, tempKey)
                                if transObject:
                                    transObject.values.append(tempVal)
                                else:
                                    translationList.append(Translation(tempKey, [tempVal]))
                        else: continue
                else:
                    if line[:-1].endswith('*/'):
                        multiline_comment_flag = False
                    continue

    # Append to rows to write on xlsx file
    for translation in translationList:
        tempCol = [translation.key]
        for value in translation.values:
            if value == True:
                continue
            else:
                tempCol.append(value)
        rows.append(tempCol)
        
    create_xlsx_file(out_path, fields, rows)

# =========================================================================
# ++++++++++++++++++++ Generate xlsx file from Android +++++++++++++++++++++
# =========================================================================
def generate_xlsx_from_android(source_path, out_path):
    startswithFolder = "values-"
    fields = ["key"]
    rows = []
    translationList = []
    originFilePaths = []
    full_out_paths = None
    
    for root, roots, filenames in os.walk(source_path):
        endPath = os.path.basename(os.path.normpath(root))
        if (endPath.startswith(startswithFolder)):
            originFilePath = os.path.join(root, "strings.xml")
            originFilePaths.append(originFilePath)
    
    originFilePaths.sort()

    for originFilePath in originFilePaths:
        arrRootPath = originFilePath.split("/")
        dirname = arrRootPath[len(arrRootPath) - 2]
        fields.append(dirname.replace(startswithFolder, ""))
        multiline_comment_flag = False
        tempCol = []
        with open(originFilePath, "r") as f:
            for line in f:
                if not multiline_comment_flag:
                    if line.startswith('<!--') and not line[:-1].endswith('-->'):
                        multiline_comment_flag = True
                        if line[:-1].endswith('-->'):
                            multiline_comment_flag = False
                        continue
                    else:
                        line = line.split('#')[0]
                        # Empty line
                        if line == "\n":
                            continue
                        # Comment line
                        elif line and line.startswith('<!--'):
                            # Check translation key exist in translation list
                            if any(x.key == line.strip() for x in translationList):
                                continue
                            else:
                                translationList.append(Translation(line.strip(), [True]))
                        elif line:
                            lineSearch = re.search('<string name=\"(.*)\">(.*)</string>', line.strip())
                            if lineSearch:
                                tempKey = lineSearch.group(1)
                                tempVal = lineSearch.group(2)
                                transObject = find_translation(translationList, tempKey)
                                if transObject:
                                    transObject.values.append(tempVal)
                                else:
                                    translationList.append(Translation(tempKey, [tempVal]))
                        else: continue
                else:
                    if line[:-1].endswith('-->'):
                        multiline_comment_flag = False
                    continue
                    
    # Append to rows to write on xlsx file
    for translation in translationList:
        tempCol = [translation.key]
        for value in translation.values:
            if value == True:
                continue
            else:
                tempCol.append(value)
        rows.append(tempCol)
   
    create_xlsx_file(out_path, fields, rows)

# =========================================================================
# ++++++++++++++++++++++++++ Create xlsx file +++++++++++++++++++++++++++++
# =========================================================================
def create_xlsx_file(out_path, fields, values):
    full_out_paths = os.path.join(out_path, "translations.xlsx")
    
    # Create a workbook and add a worksheet.
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.append(fields)
    
    for value in values:
        text = [val.decode('utf-8') for val in value]
        worksheet.append(text)

    workbook.save(full_out_paths)

# =========================================================================
# +++++++ Standard boilerplate to call the main() function to begin +++++++
# =========================================================================
parser = argparse.ArgumentParser(description="XLSX file commands")
parser.add_argument("-p", help="Specify Platform (iOS, Android)", dest="platform", type=str, required=True)
parser.add_argument("-i", help="Input source, Iproj directories paths", dest="input", type=str, required=True)
parser.add_argument("-o", help="Generated output path for xlsx file", dest="output", type=str, required=True)

parser.add_argument("-v",
                    "--verbose",
                    help="increase output verbosity",
                    action="store_true")
args = parser.parse_args()

# Setup logging
if args.verbose:
  loglevel = logging.DEBUG
else:
  loglevel = logging.INFO

main(args, loglevel)
