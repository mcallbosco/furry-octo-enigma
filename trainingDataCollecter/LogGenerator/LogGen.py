import argparse
import json
from operator import truediv
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
    return filesToDo

def generateLogs(filestodo,rootpath,outputpath,usemethods):   
    incnumb=0           
    for file in filestodo:
        if usemethods is True:
            methods = findmethods(file,rootpath)
            if methods is None:
                break
            for method in methods:
                process1 = subprocess.run("cd " + rootpath + " && git --no-pager log --no-notes -L :" + method + ":." + file + " > "+ outputpath +"\log" + str(incnumb) +"["+method+"].txt", shell=True)
                print("Generated logs for " + file + method)
                #opens log and checks if it's 0 bytes, if so, delete it
                with open(outputpath +"\log" + str(incnumb) +"["+method+"].txt", 'r') as f:
                    data = f.read()
                if len(data) == 0:
                    os.remove(outputpath +"\log" + str(incnumb) +"["+method+"].txt") 
                    print("Deleted empty log")   
                incnumb += 1
        else:
            process1 = subprocess.run("cd " + rootpath + " && git --no-pager log --no-notes -L start,end." + file + " > "+ outputpath +"\log" + str(incnumb) +".txt", shell=True)
            print("Generated logs for " + file)
            incnumb += 1



def parseMethodsPython(file,rootpath):
    with open(rootpath+file, 'r') as f:
        data = f.read()
    methods = []
    for line in data.split('\n'):
        line = line.strip(string.whitespace)
        line.strip(" ")

        if line.startswith('def '):
            methods.append(line.split('def ')[1].split('(')[0])
    return methods

def parseMethodsJava(file,rootpath):
    with open(rootpath+file, 'r') as f:
        data = f.read()
    methods = []
    for line in data.split('\n'):
        line = line.strip(string.whitespace)
        line.strip(" ")

        if line.startswith('public '):
            splitline = line.split('public ')[1].split('(')[0].split(' ')
            splitline = splitline[len(splitline)-1].strip(";").strip("{")

            methods.append(splitline)
        elif line.startswith('private '):
            splitline = line.split('private ')[1].split('(')[0].split(' ')
            splitline = splitline[len(splitline)-1].strip(";").strip("{")
            methods.append(splitline)
        elif line.startswith('protected '):
            splitline = line.split('protected ')[1].split('(')[0].split(' ')
            splitline = splitline[len(splitline)-1].strip(";").strip("{")
            methods.append(splitline)
        
    print(methods)
    return methods

def findmethods(file,rootpath):
    #working, need to figure out how to parse methods for each file.
    if file.endswith('.py'):
        methods = parseMethodsPython(file,rootpath)
    if file.endswith('.java'):
        methods = parseMethodsJava(file,rootpath)

    return methods

def main():
    parser = argparse.ArgumentParser(description='Generates a folder of gitlogs for certain Languages from a git repo on disk. ONLY FOR BASH SYSTEMS')
    parser.add_argument('-f', '--fileformat', help='The fileformat to generate logs for according to fileformats.JSON by default', required=True)
    parser.add_argument('-p', '--path', help='The path to the git repo to generate logs for', required=True)
    parser.add_argument('-o', '--output', help='The output folder', required=True)
    parser.add_argument('-d', '--defJSON', help='the definitions of file formats', required=False)
    parser.add_argument('-m', '--methods', help='finds methods in the files to generate logs for. Buggy!!!', default=False, action="store_true")
    args = parser.parse_args()
    if args.methods is True:
        readmethods = True
        print("Reading methods")
    else:
        readmethods = False
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
    generateLogs(filesToDo,args.path,args.output,readmethods)


main()


