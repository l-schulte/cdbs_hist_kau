from datetime import datetime
import time
import math
from time import sleep
import requests
from requests.models import HTTPBasicAuth
import json

from importer.sonarqube import sonarqube_instance, metric_keys


class SonarqubeApi:

    def __init__(self, login, password):
        self.auth = HTTPBasicAuth(login, password)

    def get_token(self):

        url = sonarqube_instance + '/api/user_tokens/generate' + \
            '?name=cdbs{}'.format(time.time())

        res = None

        for i in range(20):

            try:
                res = requests.post(url, auth=self.auth)

                if res.ok:
                    self.token = res.json()['token']
                    return self.token

            except Exception:
                ''

            sleep(15)

        res.raise_for_status()

    def check_status(self, key, start_time):

        url_search = sonarqube_instance + '/api/projects/search'

        for _ in range(20):
            res_search = requests.get(url_search, {'projects': key}, auth=self.auth)
            projects = res_search.json()['components']

            if len(projects) >= 1 and 'lastAnalysisDate' in projects[0]:

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

        res_search = None

        for _ in range(3):

            try:
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

            except Exception:
                ''

            sleep(15)

        res_search.raise_for_status()

    def trigger_analysis(self, runner, commit, repo, project_key, token):

        url = 'http://{}:{}/'.format('localhost', runner['port'])
        repo['_id'] = ''
        res = requests.post(
            url,
            params={'commit': commit['commit_id'], 'project_key': project_key, 'api_key': token},
            json=json.dumps(repo))

        if res.ok:
            return res, res.text

        return res, '{} - {}'.format(res.status_code, res.reason)
