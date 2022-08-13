import argparse
import json
import os
import string
import subprocess
#INPUTS: Fileformat from fileformats.json, path to folder
#OUTPUTS: A folder of gitlogs generated from files matching the fileformat
#HELPS https://stackoverflow.com/questions/67382153/how-to-search-for-keywords-in-json

def getExtensions(db, language):
    db = next(
        (item for item in db if item["language"] == language), None
    )
    if db:
        return db["extensions"]
    return None

def searchFiles(path, fileformats):
    filesToDo = []
    for root, dirs, files in os.walk(path):
        for file in files:
            for fileformat in fileformats:
                if file.endswith(fileformat):
                    #code to generate a list of paths of files to generate logs for
                    filesToDo.append(os.path.join(root, file).removeprefix(path))
                    print(os.path.join(root, file).removeprefix(path+"\\"))
    return filesToDo

def generateLogs(filestodo,rootpath):              
    for file in filestodo:
        #working, need to figure out how to parse classes for each file.
        #parseMethodsPython(file)
        process1 = subprocess.run("cd " + rootpath + " && git --no-pager log --no-notes -- ." + file, shell=True)
        print("Generated logs for " + file)
        #git --no-pager log --no-notes -L :main:main.cc > log.txt

def parseMethodsPython(file):
    with open(file, 'r') as f:
        data = f.read()
    methods = []
    for line in data.split('\n'):
        line = line.strip(string.whitespace)
        line.strip(" ")

        if line.startswith('def '):
            methods.append(line.split('def ')[1].split('(')[0])
    print(methods)
    return methods


def main():
    parser = argparse.ArgumentParser(description='Generates a folder of gitlogs for certain Languages from a git repo on disk. ONLY FOR BASH SYSTEMS')
    parser.add_argument('-f', '--fileformat', help='The fileformat to generate logs for according to fileformats.JSON by default', required=True)
    parser.add_argument('-p', '--path', help='The path to the git repo to generate logs for', required=True)
    #parser.add_argument('-o', '--output', help='The output folder', required=True)
    parser.add_argument('-d', '--defJSON', help='the definitions of file formats', required=False)
    args = parser.parse_args()
    if args.defJSON is None:
        args.defJSON = './fileformats.json'
    with open(args.defJSON, 'r') as f:
        data = f.read()
    fileformatsdb = json.loads(data)
    fileformatsToParse = fileformatsdb["languageToAnalyze"]
    fileformats = getExtensions(fileformatsToParse,args.fileformat)
    if fileformats is None:
        print("Fileformat not found in " + args.defJSON)
        print("Available Languages:")
        for language in fileformatsToParse:
            print(language)
        return
    filesToDo = searchFiles(args.path, fileformats)
    generateLogs(filesToDo,args.path)


main()


