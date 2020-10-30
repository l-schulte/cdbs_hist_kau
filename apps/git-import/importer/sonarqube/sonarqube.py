from importer.sonarqube.cli import SonarqubeCli
from importer.sonarqube.api import SonarqubeApi
from importer.sonarqube import api_username, api_password

cli = SonarqubeCli()


def analyze(commit):
    api = SonarqubeApi(api_username, api_password)

    token = api.get_token()

    key = api.get_project_key('Test4Analysis')

    runners = cli.runners

    start_time = api.trigger_analysis(runners[0], commit, 'jabref', key, token)

    # if start_time is None or not api.check_status(key, start_time):
    #     return {
    #         'status': 'Error'
    #     }

    # analysis_result = api.get_analysis_result(key)

    # return analysis_result

    return start_time
