from sonarqube.runner import GradleRunner
from sonarqube.api import SonarqubeApi
from sonarqube import API_USERNAME, API_PASSWORD, print_runner

gradle = GradleRunner()
api = SonarqubeApi(API_USERNAME, API_PASSWORD)

print('Loading api token.')
token = api.get_token()


def start_analysis(commit, runner, repo):

    key = api.get_project_key(runner)

    res, start_time = api.trigger_analysis(runner, commit, repo, key, token)

    gradle.unlock_runner(runner)

    return res, start_time


def read_analysis(start_time, runner):

    key = api.get_project_key(runner)

    print_runner(runner, 'Waiting for results.')

    if start_time is None or not api.check_status(key, start_time):

        print_runner(runner, 'Could not read results')
        return {
            'status': False
        }

    print_runner(runner, 'Results are ready.')

    analysis_result = api.get_analysis_result(key)

    print_runner(runner, 'Read results.')

    analysis_result['status'] = True

    return analysis_result


def get_runner():

    return gradle.lock_runner()
