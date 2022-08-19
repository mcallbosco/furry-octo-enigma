import argparse
import json
from operator import truediv
import os
import string
import subprocess
#INPUTS: Fileformat from fileformats.json, path to folder
#OUTPUTS: A folder of gitlogs generated from files matching the fileformat
#HELPS https://stackoverflow.com/questions/67382153/how-to-search-for-keywords-in-json

verbose = False

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
            methods = parseMethodsCtags(file,rootpath)
            if methods is None:
                break
            for method in methods:
                outputname = str(file).split("\\")[len(str(file).split("\\")) - 1].split(".")[0] +"["+method+"].gitlog"
                process1 = subprocess.run("cd " + rootpath + " && git --no-pager log --no-notes -L :" + method + ":." + file + " > "+ outputpath +"\\" +  outputname, shell=True)
                print("Generated logs for " + file + "[" + method + "]")
                #opens log and checks if it's 0 bytes, if so, delete it
                with open(outputpath +"\\" + outputname, 'r') as f:
                    data = f.read()
                if len(data) == 0:
                    os.remove(outputpath +"\\" + outputname)
                    print("Deleted empty log")   
                incnumb += 1
        else:
            outputname = str(file).split("\\")[len(str(file).split("\\")) - 1].split(".")[0] +"["+method+"].gitlog"
            process1 = subprocess.run("cd " + rootpath + " && git --no-pager log --no-notes --patch ." + file + " > "+ outputname, shell=True)
            print("Generated logs for " + file)
            incnumb += 1
    print("Generated " + str(incnumb) + " logs")




def parseMethodsCtags(file,rootpath):
    process1 = subprocess.run("ctags.exe -x " +rootpath+file , stdout=subprocess.PIPE)
    output = process1.stdout.decode('utf-8')
    methods = []
    for line in output.split('\n'):
        line = line.split(" ")[0]
        if line != "":
            methods.append(line)
    if verbose:
        print (methods)
    return methods

def logGen(fileformats,path,output,defJSON,usemethods):
    with open(defJSON, 'r') as f:
        data = f.read()
    fileformatsdb = json.loads(data)
    fileformatsToParse = fileformatsdb["languageToAnalyze"]
    fileformats = getExtensions(fileformatsToParse,fileformats)
    if fileformats is None:
        print("Fileformat not found in " + defJSON)
        print("Available Languages:")
        for language in fileformatsToParse:
            print(language)
        return None
    filesToDo = searchFiles(path, fileformats)
    generateLogs(filesToDo,path,output,usemethods)
    return True

def main():
    parser = argparse.ArgumentParser(description='Generates a folder of gitlogs for certain Languages from a git repo on disk. ONLY FOR BASH SYSTEMS')
    parser.add_argument('-f', '--fileformat', help='The fileformat to generate logs for according to fileformats.JSON by default', required=True)
    parser.add_argument('-p', '--path', help='The path to the git repo to generate logs for', required=True)
    parser.add_argument('-o', '--output', help='The output folder', required=True)
    parser.add_argument('-d', '--defJSON', help='the definitions of file formats', required=False)
    parser.add_argument('-m', '--methods', help='finds methods in the files to generate logs for. Buggy!!! Supports languages and files ctags supports', default=False, action="store_true")
    args = parser.parse_args()
    if args.defJSON is None:
        args.defJSON = './fileformats.json'
    logGen(args.fileformat,args.path,args.output,args.defJSON,args.methods)
    
    """
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
    generateLogs(filesToDo,args.path,args.output,args.methods)
    """

#main()










''' OLD HARDCODED METHOD FINDER. NOW USING ctags 
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
    
    #OLD HARDCODED CRAP
    #working, need to figure out how to parse methods for each file.
    if file.endswith('.py'):
        methods = parseMethodsPython(file,rootpath)
    if file.endswith('.java'):
        methods = parseMethodsJava(file,rootpath)
    if file.endswith('.c' or '.cpp'):
        methods = parseMethodsC(file,rootpath)
    return methods
    
'''


