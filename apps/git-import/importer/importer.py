from importer.git import git
from importer import db

repos = list(db.repos.find())


def go():
    for repo in repos:
        git.start(repo)
