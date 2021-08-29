#!/usr/bin/env python
import sys, argparse, logging, os, csv

PLATFORM = None
IN_PATH = None
OUT_PATH = None
LANG_KEYS = None  # static will change later

# Gather our code in a main() function
def main(args, loglevel):
    logging.basicConfig(format="%(message)s", level=loglevel)
    PLATFORM = args.platform
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
    logging.debug("Valid source path, finding csv file ...")
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
    
    logging.debug("\n")
    if PLATFORM == "ios":
        logging.debug("Platform : %s" % PLATFORM)
    elif PLATFORM == "android":
        logging.debug("Platform : %s" % PLATFORM)
    else:
        logging.warn("Invalid platform, platform should be ios, android.")
        logging.debug("\n")
        logging.error('ERROR LOCALIZING.\n')
        return
    
    logging.info("Generated output directory: %s" % OUTPUT_DIR)
    generate_keys(IN_PATH, OUTPUT_DIR, PLATFORM)
    print('\n')
    logging.info("DONE LOCALIZING.\n")

def generate_keys(source_path, output, platform):
    base_out_dir = output
    full_out_paths = None
    allwrites = None
    
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
                
                # remove the first element in first row cause this has value 'key'
                line = first_row[1:]
                LANG_KEYS = line  # assign new value to key
                
                # iterate each language
                lang_path = ""
                for lang in LANG_KEYS:
                    if platform == "ios":
                        lang_path = os.path.join(base_out_dir, "{0}.lproj/".format(lang))
                
                    if platform == "android":
                        lang_path = os.path.join(base_out_dir, "values-{0}/".format(lang))
                
                    # Generate directory per language key
                    if not os.path.exists(lang_path):
                        os.makedirs(lang_path)
                
                
            if platform == "ios":
                full_out_paths = [os.path.join(base_out_dir, "{0}.lproj/".format(langKey) + "Localizable.strings") for langKey in LANG_KEYS]
            if platform == "android":
                full_out_paths = [os.path.join(base_out_dir, "values-{0}/".format(langKey) + "strings.xml") for langKey in LANG_KEYS]
                
        allwrites = [open(out_path, 'w') for out_path in full_out_paths]
                
        if platform == "ios":
            start_localize_ios(source_path, allwrites, LANG_KEYS)
        if platform == "android":
            start_localize_android(source_path, allwrites, LANG_KEYS)
            
# =========================================================================
# ++++++++++++++++++++++++ Check available ++++++++++++++++++++++++++++++++
# =========================================================================
def check_availability(element, collection):
    return element in collection
            
# =========================================================================
# ++++++++++++++++++++++++++++++ iOS ++++++++++++++++++++++++++++++++++++++
# =========================================================================
def start_localize_ios(source_path, all_writes, lang_keys):
    allwrites = all_writes
            
    for dirname, dirnames, filenames in os.walk(source_path):
        for f in filenames:
            filename, ext = os.path.splitext(f)
            if ext != '.csv':
                continue
        
            fullpath = os.path.join(dirname, f)
        
            with open(fullpath, 'rt', encoding='utf8') as csvfile:
                # Header
                [fwrite.write('/*\n Localizable.strings\n*/\n') for fwrite in allwrites]
        
                reader = csv.reader(csvfile, delimiter=',')
                iterrows = iter(reader)
                next(iterrows) # skip first line (it is header).
        
                my_list = ['']
                for row in iterrows:
                    row_key = row[0]
            
                    # comment
                    if row_key == '':
                        continue
                    elif row_key[:2] == '/*':
                        [fwrite.write('\n{key}\n'.format(key=row[0])) for fwrite in allwrites]
                        continue
                    # check contains
                    elif check_availability(row_key, my_list):
                        continue
            
                    my_list.append(row_key)
                    row_values = [row[i+1] for i in range(len(lang_keys))]
                    # if any row is empty, skip it!
                    if any([value == '' for value in row_values]):
                        [fwrite.write('\n') for idx, fwrite in enumerate(allwrites)]
                    else:
                        [fwrite.write('"{key}" = "{lang}";\n'.format(key=row_key, lang=row_values[idx])) for idx, fwrite in enumerate(allwrites)]
    [fwrite.close() for fwrite in allwrites]
            
            
            
# =========================================================================
# ++++++++++++++++++++++++++++++ Android ++++++++++++++++++++++++++++++++++
# =========================================================================
def start_localize_android(source_path, all_writes, lang_keys):
    allwrites = all_writes
    
    [fwrite.write('<?xml version="1.0" encoding="utf-8"?>\n') for fwrite in allwrites]
    [fwrite.write('<resources>') for fwrite in allwrites]
    
    for dirname, dirnames, filenames in os.walk(source_path):
        for f in filenames:
            filename, ext = os.path.splitext(f)
            if ext != '.csv':
                continue
        
            fullpath = os.path.join(dirname, f)
        
            with open(fullpath, 'rt', encoding='utf8') as csvfile:
                # Header
                [fwrite.write('\n<!--\n Localizable.strings\n-->\n') for fwrite in allwrites]
        
                reader = csv.reader(csvfile, delimiter=',')
                iterrows = iter(reader)
                next(iterrows) # skip first line (it is header).
        
                my_list = ['']
                for row in iterrows:
                    row_key = row[0]
            
                    if row_key == '':
                        continue
                    # comment
                    elif row_key[:2] == '/*':
                        [fwrite.write('\n<!-- {key} -->\n'.format(key=row_key.replace("/*", "").replace("*/", ""))) for fwrite in allwrites]
                        continue
                    # check contains
                    elif check_availability(row_key, my_list):
                        continue
            
                    my_list.append(row_key)
                    row_values = [row[i+1] for i in range(len(lang_keys))]
                    # if any row is empty, skip it!
                    if any([value == '' for value in row_values]):
                        [fwrite.write('\n') for idx, fwrite in enumerate(allwrites)]
                    else:
                        [fwrite.write('\t<string name="{key}">{lang}</string>\n'.format(key=row_key, lang=row_values[idx])) for idx, fwrite in enumerate(allwrites)]
                [fwrite.write('</resources>') for fwrite in allwrites]
    [fwrite.close() for fwrite in allwrites]
        
# =========================================================================
# +++++++ Standard boilerplate to call the main() function to begin +++++++
# =========================================================================
parser = argparse.ArgumentParser(description="Locatization commands")
parser.add_argument("-p", help="Specify Platform (iOS, Android)", dest="platform", type=str, required=True)
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
