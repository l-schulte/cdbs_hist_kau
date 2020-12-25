import subprocess
import json
from __init__ import b2s


class ClocCli:

    def get_stat(self, file, content):
        """Run a CLOC analysis on a file, return data as JSON.

        """

        command = 'cloc --json {}'.format(file.name)
        res = subprocess.run(command, capture_output=True)

        if res.returncode == 0:
            string = b2s(res.stdout)
            if string:
                return json.loads(string)

        return {'SUM': {'blank': 0, 'comment': 0, 'code': 0, 'nFiles': 1}}
