import subprocess
import os
import time
from typing import Container

from importer.sonarqube import sonarqube_instance, workdir, JOBS


def b2s(byte):
    return '' if not byte else byte.decode("utf-8")


class SonarqubeCli:

    runners = []
    containers = []

    def __init__(self):
        self.start_containers()

    def __del__(self):
        self.stop_containers()

    def start_containers(self):

        sq_command = 'docker run -d --rm --name sonarqube '\
            + '-e SONAR_ES_BOOTSTRAP_CHECKS_DISABLE=true ' \
            + '-p 9000:9000 sonarqube:8-community'

        res = subprocess.run(sq_command, capture_output=True)
        self.containers.append(b2s(res.stdout))

        runner_build_command = 'docker build -t gradle_runner apps/gradle-runner/'

        subprocess.run(runner_build_command)

        runner_command = 'docker run -d --rm --name {} -p {}:5000 gradle_runner'

        for i in range(JOBS):
            runner_name = 'gradle_runner_{}'.format(i)
            runner_port = '5004{}'.format(i)
            res = subprocess.run(runner_command.format(runner_name, i), capture_output=True)
            runner_id = b2s(res.stdout)
            self.runners.append({'name': runner_name, 'id': runner_id, 'port': runner_port})
            self.containers.append(runner_id)

        print(self.containers)

    def stop_containers(self):

        for id in self.containers:
            command = 'docker stop {}'.format(id[:12])
            subprocess.run(command)
