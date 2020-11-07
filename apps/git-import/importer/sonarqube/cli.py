import subprocess
import threading

from importer.sonarqube import JOBS


def b2s(byte):
    return '' if not byte else byte.decode("utf-8")


class SonarqubeCli:

    __runners = []
    __lock = None
    __idle_runners = []
    containers = []

    def __init__(self):
        self.__lock = threading.Lock()
        self.start_containers()

    def __del__(self):
        self.stop_containers()

    def __sem_lock(self, b):
        if b:
            self.__lock.acquire()
        else:
            self.__lock.release()

    def lock_runner(self):

        self.__sem_lock(True)

        runner = None

        if len(self.__idle_runners) > 0:
            runner = self.__idle_runners.pop()

        self.__sem_lock(False)
        return runner

    def start_containers(self):

        self.__sem_lock(True)

        net_command = 'docker network create --driver bridge sonarqube_network'
        res = subprocess.run(net_command, capture_output=True)

        sq_command = 'docker run -d --rm --name sonarqube '\
            + '-e SONAR_ES_BOOTSTRAP_CHECKS_DISABLE=true ' \
            + '--net=sonarqube_network ' \
            + '-p 9000:9000 sonarqube:8-community'

        res = subprocess.run(sq_command, capture_output=True)
        self.containers.append(b2s(res.stdout))

        runner_build_command = 'docker build -t gradle_runner apps/gradle-runner/'

        subprocess.run(runner_build_command)

        runner_command = 'docker run -d --rm --net=sonarqube_network --name {} -p {}:5000 gradle_runner'

        for i in range(JOBS):
            runner_name = 'gradle_runner_{}'.format(i)
            runner_port = 50040 + i
            res = subprocess.run(runner_command.format(runner_name, runner_port), capture_output=True)
            runner_id = b2s(res.stdout)
            self.__runners.append({'name': runner_name, 'id': runner_id, 'port': runner_port})
            self.containers.append(runner_id)

        self.__idle_runners = self.__runners
        print(self.containers)

        self.__sem_lock(False)

    def stop_containers(self):

        self.__sem_lock(True)

        for id in self.containers:
            command = 'docker stop {}'.format(id[:12])
            subprocess.run(command)

        self.containers = []
        self.__idle_runners = []
        self.__runners = []

        self.__sem_lock(False)

    def unlock_runner(self, runner):

        self.__sem_lock(True)

        self.__idle_runners.append(runner)

        self.__sem_lock(False)
