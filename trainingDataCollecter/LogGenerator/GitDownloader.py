import git
import argparse
import json

#downloads a repo


def main():
    parser = argparse.ArgumentParser(description='Downloads a Repo')
    parser.add_argument('-r', '--repo', help='The Repo to Download', required=True)
    parser.add_argument('-o', '--output', help='The output folder', required=True)
    args = parser.parse_args()

    repo = git.Repo.clone_from(args.repo, args.output)