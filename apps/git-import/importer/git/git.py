import datetime

from importer import db_log
from importer.git import interpreter
from importer.git.cli import GitCli


def crawl(repo):

    db_log.insert_one({'text': 'Import for repo {}'.format(repo['title']),
                       'time': datetime.datetime.now()})

    cli = GitCli(repo)

    cli.clone()
    cli.pull()

    log = cli.log()
    return interpreter.log(log)


def get_file_content(repo, commit_id, path):

    cli = GitCli(repo)

    return cli.show(commit_id, path)


def checkout_commit(repo, commit_id):

    cli = GitCli(repo)

    return cli.checkout(commit_id)
