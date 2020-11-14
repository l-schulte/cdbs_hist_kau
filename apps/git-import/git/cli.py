import os
import subprocess
import datetime

from __init__ import db_log
from git import workdir


def b2s(byte):
    return '' if not byte else byte.decode("utf-8")


class GitCli:

    def __init__(self, repo):
        self.repo = repo

    def clone(self):

        os.chdir('repos')

        command = 'git clone {}'.format(self.repo['url'])
        res = subprocess.run(command,
                             capture_output=True)

        db_log.insert_one({'text': command,
                           'time': datetime.datetime.now(),
                           'data': {
                               'repo': self.repo['_id'],
                               'error': b2s(res.stderr),
                               'output': b2s(res.stdout)
                           }})

        os.chdir(workdir)

    def checkout(self, commit_id):

        os.chdir('repos/{}'.format(self.repo['title']))

        command = 'git checkout {}'.format(commit_id)
        res = subprocess.run(command, capture_output=True)

        os.chdir(workdir)

        return res

    def pull(self):

        os.chdir('repos/{}'.format(self.repo['title']))

        command = 'git pull --all'
        res = subprocess.run(command, capture_output=True)

        db_log.insert_one({'text': command,
                           'time': datetime.datetime.now(),
                           'data': {
                               'repo': self.repo['_id'],
                               'error': b2s(res.stderr),
                               'output': b2s(res.stdout)
                           }})

        os.chdir(workdir)

    def log(self):

        os.chdir('repos/{}'.format(self.repo['title']))

        command = 'git log --numstat --no-merges --date=unix'
        res = subprocess.run(command, capture_output=True)

        os.chdir(workdir)

        return b2s(res.stdout).splitlines()

    def show(self, commit_id, path):

        os.chdir('repos/{}'.format(self.repo['title']))

        command = 'git show {}:{}'.format(commit_id, path)
        res = subprocess.run(command, capture_output=True)

        os.chdir(workdir)

        if res.returncode == 0:
            return b2s(res.stdout)
        else:
            return ''
