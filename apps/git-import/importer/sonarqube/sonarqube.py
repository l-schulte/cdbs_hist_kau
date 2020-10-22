from importer.sonarqube.cli import SonarqubeCli
from importer.sonarqube.api import SonarqubeApi


def go():
    cli = SonarqubeCli()
    api = SonarqubeApi('admin', 'admin')

    token = api.get_token()

    key = api.get_project_key('Test4Analysis')

    start_time = cli.analyze('jabref', key, token)

    res = api.check_status(key, start_time)

    print(res)
