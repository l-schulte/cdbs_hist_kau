from copy import Error
from importer.sonarqube.cli import SonarqubeCli
from importer.sonarqube.api import SonarqubeApi
from importer.sonarqube import api_username, api_password


def go():
    cli = SonarqubeCli()
    api = SonarqubeApi(api_username, api_password)

    token = api.get_token()

    key = api.get_project_key('Test4Analysis')

    start_time = cli.analyze('jabref', key, token)

    if not api.check_status(key, start_time):
        raise Error('Analysis not complete after timer ran out')

    analysis_result = api.get_analysis_result(key)

    return analysis_result
