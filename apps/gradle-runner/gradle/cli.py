import subprocess
import os
import time

from gradle import sonarqube_instance, workdir


def b2s(byte):
    return '' if not byte else byte.decode("utf-8")


class GradleCli:

    def analyze(self, project, project_key, token):

        os.chdir('repos/{}'.format(project))

        build_file = open("build.gradle", "r")
        content = build_file.read()

        if 'id "org.sonarqube" version "2.7"' not in content:
            print(
                '>> id "org.sonarqube" version "2.7" << missing in build.gradle file...')
            return False

        command = './gradlew -x test testClasses sonarqube ' + \
            '-D sonar.projectKey={} -D sonar.host.url={} -D sonar.login={}'\
            .format(project_key, sonarqube_instance, token)

        start_time = time.time()

        res = subprocess.run(command, capture_output=True)

        os.chdir(workdir)

        if not res.returncode == 0:
            print(b2s(res.stdout))
            return None

        return start_time
