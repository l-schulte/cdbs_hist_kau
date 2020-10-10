import subprocess
import json


def b2s(byte):
    return '' if not byte else byte.decode("utf-8")


class ClocCli:

    # def __init__(self):
    #     print('init not implemented')

    def get_stat(self, file, content):

        command = 'cloc --json {}'.format(file.name)
        res = subprocess.run(command, capture_output=True)

        if res.returncode == 0:
            string = b2s(res.stdout)
            if string:
                return json.loads(string)

        return {'SUM': {'blank': 0, 'comment': 0, 'code': 0, 'nFiles': 1}}
