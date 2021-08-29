DIR=$(PWD)
RESOURCE=$(PWD)/Resources/

csv2ios: generate-ios-from-csv
xlsx2ios: generate-ios-from-xlsx
ios2csv: generate-csv-file-ios
ios2xlsx: generate-xlsx-file-ios
csv2android: generate-android-from-csv
xlsx2android: generate-android-from-xlsx
android2csv: generate-csv-file-android
android2xlsx: generate-xlsx-file-android

csv2json: generate-csv-json-file
xlsx2json: generate-xlsx-json-file

generate-ios-from-csv:
	python3 $(RESOURCE)csv2strings.py -p ios -i $(DIR)/Input -o $(DIR)

generate-ios-from-xlsx:
	python3 $(RESOURCE)xlsx2strings.py -p ios -i $(DIR)/Input -o $(DIR)

generate-csv-file-ios:
	python3 $(RESOURCE)strings2csv.py -p ios -i $(DIR)/Input -o $(DIR)

generate-xlsx-file-ios:
	python3 $(RESOURCE)strings2xlsx.py -p ios -i $(DIR)/Input -o $(DIR)

generate-android-from-csv:
	python3 $(RESOURCE)csv2strings.py -p android -i $(DIR)/Input -o $(DIR)

generate-android-from-xlsx:
	python3 $(RESOURCE)xlsx2strings.py -p android -i $(DIR)/Input -o $(DIR)

generate-csv-file-android:
	python3 $(RESOURCE)strings2csv.py -p android -i $(DIR)/Input -o $(DIR)

generate-xlsx-file-android:
	python3 $(RESOURCE)strings2xlsx.py -p android -i $(DIR)/Input -o $(DIR)

generate-csv-json-file:
	python3 $(RESOURCE)csv2json.py -i $(DIR)/Input -o $(DIR)

generate-xlsx-json-file:
	python3 $(RESOURCE)xlsx2json.py -i $(DIR)/Input -o $(DIR)
