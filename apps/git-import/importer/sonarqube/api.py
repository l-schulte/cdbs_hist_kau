from datetime import datetime
import time
import math
from time import sleep
import requests
from requests.models import HTTPBasicAuth
import progressbar

from importer.sonarqube import sonarqube_instance, metric_keys


class SonarqubeApi:

    def __init__(self, login, password):
        self.auth = HTTPBasicAuth(login, password)

    def get_token(self):

        url = sonarqube_instance + '/api/user_tokens/generate' + \
            '?name=cdbs{}'.format(time.time())

        res = None

        for _ in progressbar.progressbar(range(20)):

            try:
                res = requests.post(url, auth=self.auth)

                print(res.ok)

                if res.ok:
                    self.token = res.json()['token']
                    return self.token

            except Exception:
                ''

            sleep(15)

        res.raise_for_status()

    def check_status(self, key, start_time):

        url_search = sonarqube_instance + '/api/projects/search'

        for _ in progressbar.progressbar(range(20)):
            res_search = requests.get(url_search, {'projects': key}, auth=self.auth)
            projects = res_search.json()['components']

            if len(projects) == 1:
                time_string = projects[0]['lastAnalysisDate']
                time_string = time_string[:-2] + ':' + time_string[-2:]
                run_time = datetime.fromisoformat(time_string).timestamp()

                if abs(run_time - start_time) < 100:
                    return True

            sleep(15)

        return False

    def get_analysis_result(self, key):

        url = sonarqube_instance + '/api/measures/component_tree'

        page = 0
        pages = 1
        page_size = 500

        base_component = {}
        components = []

        while page < pages:

            page += 1

            parameters = {
                'p': page,
                'ps': page_size,
                'component': key,
                'metricKeys': metric_keys
            }

            res = requests.get(url, parameters)
            res.raise_for_status()

            body = res.json()

            pages = math.ceil(body['paging']['total'] / page_size)

            base_component = body['baseComponent']['measures']
            components.extend(body['components'])

        return {
            'base': base_component,
            'files': components
        }

    def get_project_key(self, key):

        url_search = sonarqube_instance + '/api/projects/search'
        res_search = requests.get(url_search, {'projects': key}, auth=self.auth)

        if res_search.ok:

            projects = res_search.json()['components']

            if len(projects) == 1:
                return key

            url_create = sonarqube_instance + '/api/projects/create' + \
                '?name={}&project={}'.format(key, key)

            res_create = requests.post(url_create, auth=self.auth)

            if res_create.ok:
                return res_create.json()['project']['key']

            res_create.raise_for_status()

        res_search.raise_for_status()

    def trigger_analysis(self, runner, commit, project, project_key, token):

        url = 'http://{}:{}/'.format('localhost', runner['port'])
        print(url)
        res = requests.get(url, {'target': project, 'commit': commit, 'project_key': project_key, 'api_key': token})

        print(res)
