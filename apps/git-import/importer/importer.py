from importer.git import git
from importer import db, db_commits, db_files

repos = list(db.repos.find())


def __store_commits(repo, commits):

    for commit in commits:
        commit['repo'] = repo.target['_id']

    db_commits.insert_many(commits)


def __store_changes(repo, changes):

    for change in changes:

        db_files.update_one({
            'path': change['old_path']
        }, {
            '$set': {
                'path': change['path'],
                'repo': repo.target['_id']
            },
            '$push': {
                'changes': change
            }
        }, True)


def __calculate_metrics(repo):

    content = repo.show(change['commit_id'], change['path'])

    print('not implemented')


def go():
    for repo in repos:

        commits, changes = git.crawl(repo)

        __store_commits(repo, commits)
        __store_changes(repo, changes)
