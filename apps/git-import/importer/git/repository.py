import os
import subprocess
import datetime

from importer import log
from importer.git import workdir


class Repo:

    def __init__(self, target):
        self.target = target

    def clone(self):

        os.chdir('repos')

        command = 'git clone {}'.format(self.target['url'])
        res = subprocess.run(command,
                             capture_output=True)

        log.insert_one({'text': command,
                        'time': datetime.datetime.now(),
                        'data': {
                            'target': self.target['_id'],
                            'error': str(res.stderr),
                            'output': str(res.stdout)
                        }})

        os.chdir(workdir)

    def pull(self):

        os.chdir('repos/{}'.format(self.target['title']))

        command = 'git pull --all'
        res = subprocess.run(command)

        log.insert_one({'text': command,
                        'time': datetime.datetime.now(),
                        'data': {
                            'target': self.target['_id'],
                            'error': str(res.stderr),
                            'output': str(res.stdout)
                        }})

        os.chdir(workdir)
