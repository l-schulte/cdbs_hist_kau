import datetime

from importer import db_log
from importer.git import interpreter
from importer.git.cli import GitCli


def crawl(target):

    db_log.insert_one({'text': 'Import for repo {}'.format(target['title']),
                       'time': datetime.datetime.now()})

    repo = GitCli(target)

    repo.clone()
    repo.pull()

    log = repo.log()
    return interpreter.log(log)
