from textblob import TextBlob
import csv
import sys
import time
import datetime
from textstat.textstat import textstat

inputfile = "INPUT FILE"
textcol = 7
textcoltitle = "TEXT OF SPEECH"

output = csv.writer(open("readinglevel-"+inputfile, 'wt')) 

def get_reading(line):
	row = line
	test_data = line[textcol]
	try:
		flesch_kincaid_grade = str(textstat.flesch_reading_ease(test_data))
		gunning_fog = str(textstat.gunning_fog(test_data))
		smog_index = str(textstat.smog_index(test_data))
		automated_readability_index = str(textstat.automated_readability_index(test_data))
		linsear_write_formula = str(textstat.linsear_write_formula(test_data))
		dale_chall_readability_score = str(textstat.dale_chall_readability_score(test_data))
		coleman_liau_index = str(textstat.coleman_liau_index(test_data))
		consensus = str(textstat.text_standard(test_data))
		output.writerow(row+[flesch_kincaid_grade,gunning_fog,smog_index,automated_readability_index,linsear_write_formula,dale_chall_readability_score,coleman_liau_index,consensus])
	except Exception:
		sys.exc_clear()

with open("data/"+inputfile) as f:
	reader = csv.reader(f, delimiter=",")
	for line in reader:
		if line[textcol]==textcoltitle:
			output.writerow(line+["flesch_kincaid_grade","gunning_fog","smog_index","automated_readability_index","linsear_write_formula","dale_chall_readability_score","coleman_liau_index","consensus"])
		else:
			get_reading(line)
