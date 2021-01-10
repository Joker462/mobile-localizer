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

generate-ios-from-csv:
	python $(RESOURCE)csv2strings.py -p ios -i $(DIR)/Input -o $(DIR)

generate-ios-from-xlsx:
	python $(RESOURCE)xlsx2strings.py -p ios -i $(DIR)/Input -o $(DIR)

generate-csv-file-ios:
	python $(RESOURCE)strings2csv.py -p ios -i $(DIR)/Input -o $(DIR)

generate-xlsx-file-ios:
	python $(RESOURCE)strings2xlsx.py -p ios -i $(DIR)/Input -o $(DIR)

generate-android-from-csv:
	python $(RESOURCE)csv2strings.py -p android -i $(DIR)/Input -o $(DIR)

generate-android-from-xlsx:
	python $(RESOURCE)xlsx2strings.py -p android -i $(DIR)/Input -o $(DIR)

generate-csv-file-android:
	python $(RESOURCE)strings2csv.py -p android -i $(DIR)/Input -o $(DIR)

generate-xlsx-file-android:
	python $(RESOURCE)strings2xlsx.py -p android -i $(DIR)/Input -o $(DIR)

