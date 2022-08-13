#Get an input git log and output a new directory which contains another directory for each commit.
#Each commit directory contains a file with the full method found in the commit.
#The folder name is based on how many commits since the first (First is 0).
#There will be another file to go along it which will be a JSON file with the commit information.
#The JSON file will have the following information:
#	- commit hash
#	- author
#	- commit name
#	- commit description
#   - how many commits it's been since the first commit (again start at 0)


import os
import sys

def load_commit_log(file):
    with open(file, 'r') as f:
        return f.read()

def parse_commit_diff(diff):
    if (diff.startswith('-')):
        return ''
    else: 
        return str(diff[1:])

def parse_commit_log(log):
    commits = []
    current_commit = None
    incommit = False
    current_file = None
    for line in log.split('\n'):
        if line.startswith('commit'):
            if current_commit != None:
                commits.append(current_commit)
                current_commit = None
                incommit = False
            current_commit = {}
            current_commit['hash'] = line.split()[1]
            current_commit['commitcontent'] = ''
        elif incommit:
            current_commit['commitcontent'] =  str(current_commit['commitcontent']) + str(parse_commit_diff(line)) + '\n'
        elif line.startswith('Author:'):
            current_commit['author'] = line.split(':')[1].strip()
        elif line.startswith('Date:'):
            current_commit['date'] = line.split(':')[1].strip()
            current_commit['summary'] = NULL
        elif line.startswith('    '):
            if current_commit['summary'] is NULL:
                current_commit['summary'] = line.strip()
                current_commit['description'] = NULL
            else:
                #description parser
                if (not line == '    '):
                    current_commit['description'] = str(current_commit['description']) + '\n' + str(line.strip())
        elif line.startswith('@@'):
            incommit = True
    commits.append(current_commit)
    return commits

def main():
    file = './gitlog.txt'
    output = './gitlog/'
    lengthOfargv = len(sys.argv)
    if lengthOfargv > 1 and sys.argv[1] == '-h':
        print("Usage: gitlog.py <path to log file> <path to output directory>")
        exit(0)
    else:
        if lengthOfargv > 1:
            file = sys.argv[1]
        if lengthOfargv > 2:
            output = sys.argv[2]


    log = load_commit_log(file)
    commits = parse_commit_log(log)
    
    #write commits to files
    os.makedirs(output, exist_ok=True)
    for i in range(len(commits)):
        with open(output + str(i) + '.txt', 'w') as f:
            f.write(commits[i]['commitcontent'])
        commits[i].pop('commitcontent')
        with open(output + str(i) + '.json', 'w') as f:
            f.write(str(commits[i]) + '\n')
main()
