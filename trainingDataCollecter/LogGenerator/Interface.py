import argparse
import GitDownloader as GitDownloader
import LogGen as LogGen
import shutil
import stat
import json

#https://seart-ghs.si.usi.ch/








def interfacer(repo,output,branch,submodules,multibranch,defJSON,usemethods,fileformat,seart):
    if (seart):
        seartParse(repo,output,branch,submodules,multibranch,defJSON,usemethods,fileformat,seart)
        exit()
    branches = GitDownloader.downloadRepo(repo, output+"\git", branch, multibranch, submodules)
    LogGen.logGen(fileformat, output+"\git\main", output+"\log\main", defJSON, usemethods)
    gitpath = output + '\git'
    try:
        shutil.rmtree(gitpath)
    except OSError as error:
        print("error deleting!!!")

    if multibranch is not False:
        for branch in branches:
            if ("->" in branch):
                continue 
            if (branch == 'master'):
                continue 
            print (branch)
            GitDownloader.downloadRepo(repo, output+"\git", branch, False, submodules)
            LogGen.logGen(fileformat, output+"\git\\"+branch , output+"\log\\"+branch , defJSON, usemethods)
    #else:
        #LogGen.main(repo, output, branch, defJSON)


def seartParse(repo,output,branch,submodules,multibranch,defJSON,usemethods,fileformat,seart):
    f = open(repo, encoding="utf8")
    # returns JSON object as
    # a dictionary
    data = json.load(f)
    for i in data['items']:
        gitname = i['name']
        gitrepo = "https://github.com/" + gitname + ".git"
        interfacer(gitrepo,output+"\\"+gitname.split("/")[1],branch,submodules,multibranch,defJSON,usemethods,fileformat,False)
        a = open(output+"\\"+gitname.split("/")[1]+"\gitinfo.txt", "w")
        a.write(json.dumps(i))
        a.close()
    f.close()


def main():
    parser = argparse.ArgumentParser(description='The thing that makes LogGen and GitDownloader work together')
    parser.add_argument('-r', '--repo', help='The Repo to generate logs for (Assumes internet repos)', required=True)
    parser.add_argument('-o', '--output', help='The output folder', required=True)
    parser.add_argument('-b', '--branch', help='Specify the branch', required=False)
    parser.add_argument('-s', '--submodules', help='Download submodules', default=False, action="store_true")
    parser.add_argument('-mb', '--multibranch', help='use all avalable branches',  default=False, action="store_true")
    parser.add_argument('-d', '--defJSON', help='the definitions of the file formats', required=False)
    parser.add_argument('-l', '--language', help='the language to generate logs with', required=False)
    parser.add_argument('-se', '--seart', help='use a seart JSON file defined with --repo',  default=False, action="store_true")
    parser.add_argument('-m', '--methods', help='use methods temp text',  default=False, action="store_true")



    args = parser.parse_args()
    interfacer(args.repo, args.output, args.branch, args.submodules, args.multibranch, args.defJSON , args.methods, args.language, args.seart)

main()