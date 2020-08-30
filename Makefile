DIR=$(PWD)
RESOURCE=$(PWD)/Resources/

csv2ios: generate-ios
ios2csv: generate-csv-file-ios
csv2android: generate-android
android2csv: generate-csv-file-android

generate-ios:
	python $(RESOURCE)csv2strings.py -p ios -i $(DIR)/Input -o $(DIR)

generate-csv-file-ios:
	python $(RESOURCE)strings2csv.py -p ios -i $(DIR)/Input -o $(DIR)

generate-android:
	python $(RESOURCE)csv2strings.py -p android -i $(DIR)/Input -o $(DIR)

generate-csv-file-android:
	python $(RESOURCE)strings2csv.py -p android -i $(DIR)/Input -o $(DIR)
