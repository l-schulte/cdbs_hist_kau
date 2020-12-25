import threading
import requests

from sonarqube import gradle_runner_basename


class GradleRunner:

    __lock = None
    __idle_runners = []

    def __init__(self):
        self.__lock = threading.Lock()
        self.__sem_lock(True)

        self.__idle_runners = self.get_runners()

        self.__sem_lock(False)

    def __sem_lock(self, b):
        """Set the lock of the semaphore of this gradle runner.

        """
        if b:
            self.__lock.acquire()
        else:
            self.__lock.release()

    def lock_runner(self):
        """Lock this runner from being used by another process.

        """

        self.__sem_lock(True)

        runner = None

        if len(self.__idle_runners) > 0:
            runner = self.__idle_runners.pop()

        self.__sem_lock(False)
        return runner

    def get_runners(self):
        """Get runners available on the network.

        Uses dockers named instances to access the /check endpoint of possible runner names
        to check if they are up and available for use.

        """

        print('Looking for runners...')

        runners = []
        for i in range(1, 50):
            runner = gradle_runner_basename.format(i)
            try:
                if requests.get('http://{}:5000/check'.format(runner)).ok:
                    runners.append(runner)
                else:
                    break
            except Exception:
                break

        print('Found runners:')
        print(runners)
        return runners

    def unlock_runner(self, runner):
        """Unlock this runner, allowing it to be used by another process.

        """

        self.__sem_lock(True)

        self.__idle_runners.append(runner)

        self.__sem_lock(False)
