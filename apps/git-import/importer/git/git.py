import datetime

from importer import log
from importer.git import repository


def __init(repo):
    repo.clone()
    repo.pull()


def __crawl(repo):
    print('__crawl() not implemented')


def start(target):

    log.insert_one({'text': 'Git import for repo {}'.format(target['title']),
                    'time': datetime.datetime.now()})

    repo = repository.Repo(target)

    __init(repo)
    __crawl(repo)
