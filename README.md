# GitHub Commit Line Stats

Count how many lines of code you commit in your repo! (Count by file extension)

```sh
python ghcls.py --token <YOUR GITHUB TOKEN>
```

```sh
python ghcls.py -h
usage: ghcls.py [-h] -t TOKEN [-u USER] [-c CACHE]

GitHub Commit Line Stats

options:
  -h, --help         show this help message and exit
  -t, --token TOKEN  GitHub Personal Access Token
  -u, --user USER    GitHub Username (Optional)
  -c, --cache CACHE  Cache directory for commits
```