from datetime import datetime
import json
import time
from time import sleep
import requests
from requests.models import HTTPBasicAuth
import progressbar

from importer.sonarqube import sonarqube_instance


class SonarqubeApi:

    def __init__(self, login, password):
        self.auth = HTTPBasicAuth(login, password)

    def get_token(self):

        url = sonarqube_instance + '/api/user_tokens/generate' + \
            '?name=cdbs{}'.format(time.time())
        res = requests.post(url, auth=self.auth)

        if res.ok:
            self.token = json.loads(res.text)['token']
            return self.token

        res.raise_for_status()

    def check_status(self, name, start_time):

        url_search = sonarqube_instance + '/api/projects/search'

        for i in progressbar.progressbar(range(20)):
            res_search = requests.get(url_search, {'projects': name}, auth=self.auth)
            projects = json.loads(res_search.text)['components']

            if len(projects) == 1:
                time_string = projects[0]['lastAnalysisDate']
                time_string = time_string[:-2] + ':' + time_string[-2:]
                run_time = datetime.fromisoformat(time_string).timestamp
                print(run_time)
                print(start_time)

                if abs(run_time - start_time) < 100:
                    return True

            sleep(15)

        return False

    def get_project_key(self, name):

        url_search = sonarqube_instance + '/api/projects/search'
        res_search = requests.get(url_search, {'projects': name}, auth=self.auth)

        if res_search.ok:

            projects = json.loads(res_search.text)['components']

            if len(projects) == 1:
                return name

            url_create = sonarqube_instance + '/api/projects/create' + \
                '?name={}&project={}'.format(name, name)

            res_create = requests.post(url_create, auth=self.auth)

            if res_create.ok:
                return json.loads(res_create.text)['project']['key']

            res_create.raise_for_status()

        res_search.raise_for_status()
