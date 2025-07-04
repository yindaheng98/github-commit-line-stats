import pathlib
import json
from collections import defaultdict
from typing import Dict
from github import Github, Commit  # pip install PyGitHub
from github.GithubObject import NotSet
import requests
import os
import sys

GH_TOKEN = sys.argv[1]
gh = Github(GH_TOKEN)
USER = sys.argv[2] if len(sys.argv) > 2 else NotSet
user = gh.get_user(USER)

totals = defaultdict(int)


def get_additions_in_commit(commit: Commit) -> Dict[str, int]:
    totals = defaultdict(int)
    if len(commit.parents) <= 0:
        return totals  # Skip if there are no parents (first commit)
    parent = commit.parents[0].sha
    url = f"https://api.github.com/repos/{repo.full_name}/compare/{parent}...{commit.sha}"
    patch = requests.get(url, headers={"Authorization": f"token {GH_TOKEN}"}).json()
    for file in patch.get("files", []):
        lang = os.path.splitext(file["filename"])[1]  # Get file extension
        totals[lang] += file["additions"]
    return totals


for repo in user.get_repos(type="public"):
    commit_set = set()
    for branch in repo.get_branches():
        for commit in repo.get_commits(author=user.login, sha=branch.name):
            if commit.sha in commit_set:
                continue  # Skip if commit already processed
            commit_set.add(commit.sha)
            print(f"Processing {commit.sha} at {commit.commit.author.date} in {repo.name}@{branch.name}")
            for lang, addition in get_additions_in_commit(commit).items():
                totals[lang] += addition

# write JSON
pathlib.Path("ghcls.json").write_text(json.dumps(totals, indent=2))
