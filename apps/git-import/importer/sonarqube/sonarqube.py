from importer.sonarqube.cli import SonarqubeCli
from importer.sonarqube.api import SonarqubeApi
from importer.sonarqube import api_username, api_password, print_runner

cli = SonarqubeCli()
api = SonarqubeApi(api_username, api_password)

print('Loading api token.')
token = api.get_token()


def start_analysis(commit, runner, repo):

    key = api.get_project_key('{}_{}'.format(runner['name'], runner['id'][:6]))

    res, start_time = api.trigger_analysis(runner, commit, repo, key, token)

    cli.unlock_runner(runner)

    return res, start_time


def read_analysis(start_time, runner):

    key = api.get_project_key('{}_{}'.format(runner['name'], runner['id'][:6]))

    print_runner(runner, 'Waiting for results.')

    if start_time is None or not api.check_status(key, start_time):

        print_runner(runner, 'Could not read results')
        return {
            'status': 'Error'
        }

    print_runner(runner, 'Results are ready.')

    analysis_result = api.get_analysis_result(key)

    print_runner(runner, 'Read results.')

    return analysis_result


def get_runner():

    return cli.lock_runner()
