import os
import subprocess

from git import workdir


def b2s(byte):
    return '' if not byte else byte.decode("utf-8")


class GitCli:

    def __init__(self, target):
        self.target = target

        self.clone()

    def clone(self):

        os.chdir('repos')

        command = 'git clone {}'.format(self.target['url'])
        subprocess.run(command,
                       capture_output=True)

        os.chdir(workdir)

    def checkout(self, commit_id):

        os.chdir('repos/{}'.format(self.target['title']))

        command = 'git checkout {}'.format(commit_id)
        res = subprocess.run(command, capture_output=True)

        os.chdir(workdir)

        return res

    def pull(self):

        os.chdir('repos/{}'.format(self.target['title']))

        command = 'git pull --all'
        subprocess.run(command, capture_output=True)

        os.chdir(workdir)
