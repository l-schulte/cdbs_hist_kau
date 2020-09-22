import datetime

from importer import db_log, db_commits, db_files
from importer.git import repository, interpreter


def __init(repo):

    repo.clone()
    repo.pull()


def __crawl(repo):

    log = repo.log()
    commits, changes = interpreter.log(log)

    db_commits.insert_many(commits)

    for change in changes:
        db_files.update_one({
            'path': change['old_path']
        }, {
            '$set': {
                'path': change['path']
            },
            '$push': {
                'changes': change
            }
        }, True)


def start(target):

    db_log.insert_one({'text': 'Import for repo {}'.format(target['title']),
                       'time': datetime.datetime.now()})

    repo = repository.Repo(target)

    __init(repo)
    __crawl(repo)
