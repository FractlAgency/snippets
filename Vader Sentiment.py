import nltk, csv
from nltk.sentiment.vader import SentimentIntensityAnalyzer 

file_name = "FILENAME.csv" # File to analyze
coln = 8 # Column index to analyze starting at 0

sid = SentimentIntensityAnalyzer()
output = csv.writer(open(file_name.split(" - ")[0].replace(".csv","")+"_nltk-vader-sentiment.csv", 'wt')) 
isHeader = True

with open(file_name, 'r', encoding='utf-8', errors='ignore') as f:
	reader = csv.reader((line.replace('\0','') for line in f), delimiter=",")
	for line in reader:
		if isHeader:
			output.writerow(line+[line[coln]+" neg",line[coln]+" neu",line[coln]+" pos",line[coln]+" compound"])
			isHeader = False
		else:
			sentiment = sid.polarity_scores(line[coln])
			output.writerow(line+[sentiment["neg"],sentiment["neu"],sentiment["pos"],sentiment["compound"],])
