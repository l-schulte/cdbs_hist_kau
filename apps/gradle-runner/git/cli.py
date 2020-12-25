import os
import subprocess

from git import workdir


def b2s(byte):
    return '' if not byte else byte.decode("utf-8")


class GitCli:

    def __init__(self, repo):
        self.repo = repo

        if not os.path.isdir('repos'):
            os.mkdir('repos')

        self.clone()

    def clone(self):
        """Clone the repository this instance is assigned to.

        """

        os.chdir('repos')

        command = 'git clone {}'.format(self.repo['url'])
        subprocess.run(command, capture_output=True, shell=True)

        os.chdir(workdir)

    def checkout(self, commit_id):
        """Checkout a specific commit of the repository this instance is assigned to.

        """

        os.chdir('repos/{}'.format(self.repo['title']))

        command = 'git checkout -f {}'.format(commit_id)
        res = subprocess.run(command, capture_output=True, shell=True)

        os.chdir(workdir)

        print(b2s(res.stderr))

        return b2s(res.stdout)

    def pull(self):
        """Pull all branches from the repository this instance is assigned to.

        """

        os.chdir('repos/{}'.format(self.repo['title']))

        command = 'git pull --all'
        subprocess.run(command, capture_output=True, shell=True)

        os.chdir(workdir)
