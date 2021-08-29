#!/usr/bin/env python
import sys, argparse, logging, os, importlib, json, csv

# Python 3.8 and more
importlib.reload(sys)

IN_PATH = None
OUT_PATH = None
LANG_KEYS = None  # static will change later

# Gather our code in a main() function
def main(args, loglevel):
    logging.basicConfig(format="%(message)s", level=loglevel)
    IN_PATH = args.input
    OUT_PATH = args.output
    print('\n')
    logging.info("Start Localizing .... ")
    print('\n')
    logging.info("------------------------------------")
    
    # check source path
    logging.debug("\n")
    logging.debug("Validating source path ...")
    logging.debug("\n")
    if not os.path.exists(IN_PATH):
        logging.error('Source path not found, Invalid path.')
        logging.debug("\n")
        return
    logging.debug("Valid source path, finding xlsx file ...")
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
    OUTPUT_DIR = os.path.join(OUT_PATH, "Output")
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        logging.debug("Output directory generated : %s" % OUTPUT_DIR)
        logging.debug("\n")
    else:
        logging.debug("Using output directory: %s" % OUTPUT_DIR)
        logging.debug("\n")
    
    logging.debug("\n")
    
    logging.info("Generating output directory: %s" % OUTPUT_DIR)
    generate_keys(IN_PATH, OUTPUT_DIR)
    print('\n')
    logging.info("DONE LOCALIZING.\n")
        
# =========================================================================
# ++++++++++++++++++++++++ Generate Output ++++++++++++++++++++++++++++++++
# =========================================================================
def generate_keys(source_path, output_path):
    translationDict = {}
    
    for dirname, dirnames, filenames in os.walk(source_path):
        for f in filenames:
            filename, ext = os.path.splitext(f)
            if ext != '.csv':
                continue
			
            fullpath = os.path.join(dirname, f)
			# create language key
            with open(fullpath, 'rt', encoding='utf8') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                first_row = next(reader)
                line = first_row[1:]
                LANG_KEYS = line
                iterrows = iter(reader)
                next(iterrows) # skip first line (it is header)
                
                for row in iterrows:
                    row_key = row[0]
                    
                    if row_key[:2] == '/*':
                        continue
                        
                    langDict = {}
                    row_values = [row[i+1] for i in range(len(LANG_KEYS))]
                    for index in range(len(row_values)):
                        row_value = row_values[index]
                        if row_value is None:
                            continue

                        try:
                            lang = LANG_KEYS[index]
                            langDict[lang] = row_value
                        except IndexError:
                            continue
				
                    translationDict[row_key] = langDict

    # write json file
    write_json(output_path, 'languages.json', translationDict)
                    
def write_json(target_path, target_file, data):
    if not os.path.exists(target_path):
        try:
            os.makedirs(target_path)
        except Exception as e:
            print(e)
            raise
    with open(os.path.join(target_path, target_file), 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)
# =========================================================================
# +++++++ Standard boilerplate to call the main() function to begin +++++++
# =========================================================================
parser = argparse.ArgumentParser(description="Locatization commands")
parser.add_argument("-i", help="Input source, CSV file path", dest="input", type=str, required=True)
parser.add_argument("-o", help="Generated output path for localizable files", dest="output", type=str, required=True)
parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
args = parser.parse_args()
    
# Setup logging
if args.verbose:
    loglevel = logging.DEBUG
else:
    loglevel = logging.INFO
            
main(args, loglevel)
