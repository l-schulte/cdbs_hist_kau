import os
import subprocess
import datetime

from importer import db_log
from importer.git import workdir


def b2s(byte):
    return '' if not byte else byte.decode("utf-8")


class Repo:

    def __init__(self, target):
        self.target = target

    def clone(self):

        os.chdir('repos')

        command = 'git clone {}'.format(self.target['url'])
        res = subprocess.run(command,
                             capture_output=True)

        db_log.insert_one({'text': command,
                           'time': datetime.datetime.now(),
                           'data': {
                               'target': self.target['_id'],
                               'error': b2s(res.stderr),
                               'output': b2s(res.stdout)
                           }})

        os.chdir(workdir)

    def pull(self):

        os.chdir('repos/{}'.format(self.target['title']))

        command = 'git pull --all'
        res = subprocess.run(command, capture_output=True)

        db_log.insert_one({'text': command,
                           'time': datetime.datetime.now(),
                           'data': {
                               'target': self.target['_id'],
                               'error': b2s(res.stderr),
                               'output': b2s(res.stdout)
                           }})

        os.chdir(workdir)

    def log(self):

        os.chdir('repos/{}'.format(self.target['title']))

        command = 'git log --numstat --no-merges --date=unix'
        res = subprocess.run(command, capture_output=True)

        os.chdir(workdir)

        return b2s(res.stdout).splitlines()
