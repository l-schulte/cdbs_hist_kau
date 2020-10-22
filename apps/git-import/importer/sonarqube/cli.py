from copy import Error
import subprocess
import os
import time

from importer.sonarqube import sonarqube_instance, workdir


def b2s(byte):
    return '' if not byte else byte.decode("utf-8")


class SonarqubeCli:

    def __start_container(self):

        command = 'docker run -d --name sonarqube '\
            + '-e SONAR_ES_BOOTSTRAP_CHECKS_DISABLE=true ' \
            + '-p 9000:9000 sonarqube:8-community'

        subprocess.run(command)

    def analyze(self, project, project_key, token):

        os.chdir('repos/{}'.format(project))

        build_file = open("build.gradle", "r")
        content = build_file.read()

        if 'id "org.sonarqube" version "2.7"' not in content:
            print('>> id "org.sonarqube" version "2.7" << missing in build.gradle file...')
            return False

        command = 'gradlew.bat -x test testClasses sonarqube ' + \
            '-D sonar.projectKey={} -D sonar.host.url={} -D sonar.login={}'\
            .format(project_key, sonarqube_instance, token)

        start_time = time.time()
        print(start_time)

        res = subprocess.run(command)

        os.chdir(workdir)

        if not res.returncode == 0:
            print('ERROR')
            raise Error()

        return start_time
