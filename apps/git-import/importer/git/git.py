import datetime

from importer import db_log
from importer.git import interpreter
from importer.git.cli import GitCli


def crawl(target):

    db_log.insert_one({'text': 'Import for repo {}'.format(target['title']),
                       'time': datetime.datetime.now()})

    cli = GitCli(target)

    cli.clone()
    cli.pull()

    log = cli.log()
    return interpreter.log(log)


def get_file_content(target, commit_id, path):

    cli = GitCli(target)

    return cli.show(commit_id, path)


def checkout_commit(target, commit_id):

    cli = GitCli(target)

    return cli.checkout(commit_id)
