import subprocess
import os
import time

from gradle import sonarqube_instance, workdir, sonarqube_plugin


def b2s(byte):
    return '' if not byte else byte.decode("utf-8")


class GradleCli:

    def analyze(self, repo, project_key, token):

        os.chdir('repos/{}'.format(repo['title']))

        if not os.path.isfile('build.gradle'):
            return 'Missing build.gradle', 500

        build_file = open("build.gradle", "r")
        content = build_file.read()
        build_file.close()

        if sonarqube_plugin not in content:
            lines = content.splitlines()
            for i in range(len(lines)):
                if lines[i].startswith('plugins {'):
                    lines.insert(i+1, '    ' + sonarqube_plugin)
                    break

            build_file = open("build.gradle", "w")
            build_file.write('\n'.join(lines))
            build_file.close()

        command = './gradlew -x test testClasses sonarqube ' + \
            '-D sonar.projectKey={} -D sonar.host.url={} -D sonar.login={}'\
            .format(project_key, sonarqube_instance, token)

        start_time = time.time()

        res = subprocess.run(command, capture_output=True, shell=True)

        os.chdir(workdir)

        if not res.returncode == 0:
            print(b2s(res.stdout))
            return b2s(res.stdout), 500

        return str(start_time), 200
