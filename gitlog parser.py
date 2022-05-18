#Get an input git log and output a new directory which contains another directory for each commit.
#Each commit directory contains a file with the full method found in the commit.
#The folder name is based on how many commits since the first (First is 0).
#There will be another file to go along it which will be a JSON file with the commit information.
#The JSON file will have the following information:
#	- commit hash
#	- author
#	- date
#   - how many commits it's been since the first commit

file = 'gitlog.txt'
path = './'
