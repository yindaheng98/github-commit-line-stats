import pathlib
import json
from collections import defaultdict
from github import Github  # pip install PyGitHub
import requests
import os
import sys

GH_TOKEN = sys.argv[1]
gh = Github(GH_TOKEN)
user = gh.get_user("yindaheng98")

totals = defaultdict(int)

for repo in user.get_repos(type="public"):
    commit_set = set()
    for branch in repo.get_branches():
        for commit in repo.get_commits(author=user.login, sha=branch.name):
            if commit.sha in commit_set:
                continue  # Skip if commit already processed
            commit_set.add(commit.sha)
            print(f"Processing {commit.sha} at {commit.commit.author.date} in {repo.name}@{branch.name}")
            if len(commit.parents) <= 0:
                continue  # Skip if there are no parents (first commit)
            parent = commit.parents[0].sha
            url = f"https://api.github.com/repos/{repo.full_name}/compare/{parent}...{commit.sha}"
            patch = requests.get(url, headers={"Authorization": f"token {GH_TOKEN}"}).json()
            for file in patch.get("files", []):
                lang = os.path.splitext(file["filename"])[1]  # Get file extension
                totals[lang] += file["additions"]

# write JSON
pathlib.Path("ghcls.json").write_text(json.dumps(totals, indent=2))
