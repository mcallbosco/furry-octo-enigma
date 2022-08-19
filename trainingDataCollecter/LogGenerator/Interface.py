import argparse
import GitDownloader as GitDownloader
import LogGen as LogGen
#https://seart-ghs.si.usi.ch/

def interfacer(repo,output,branch,submodules,multibranch,defJSON):
    branches = GitDownloader.downloadRepo(repo, output, branch, multibranch, submodules)
    #LogGen.logGen(repo, output, branch, defJSON)
    if multibranch is not None:
        for branch in branches:
            GitDownloader.downloadRepo(repo, output, branch, False, submodules)
    #else:
        #LogGen.main(repo, output, branch, defJSON)

def main():
    parser = argparse.ArgumentParser(description='The thing that makes LogGen and GitDownloader work together')
    parser.add_argument('-r', '--repo', help='The Repo to generate logs for (Assumes internet repos)', required=True)
    parser.add_argument('-o', '--output', help='The output folder', required=True)
    parser.add_argument('-b', '--branch', help='Specify the branch', required=False)
    parser.add_argument('-s', '--submodules', help='Download submodules', default=True, action="store_false")
    parser.add_argument('-mb', '--multibranch', help='use all avalable branches',  default=False, action="store_true")
    parser.add_argument('-d', '--defJSON', help='the definitions of the file formats', required=False)

    args = parser.parse_args()
    interfacer(args.repo, args.output, args.branch, args.submodules, args.multibranch, args.defJSON)