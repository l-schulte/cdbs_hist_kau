import plotly.express as px
import pandas as pd
import pymongo

from __init__ import db_commits, db_files


def __get_file_metrics_from_commit(commit_id, path_in_commit, newer_changes):

    commit = db_commits.find_one({'commit_id': commit_id})

    if commit is None\
            or 'sonarqube' not in commit\
            or 'status' not in commit['sonarqube']\
            or commit['sonarqube']['status'] is not True:

        commit = db_commits.find_one({'date': {'$gte': commit['date']}, 'sonarqube.status': True}, sort=[
                                     ('date', pymongo.ASCENDING)])

    if commit is None or commit['sonarqube']['status'] == 'Error':
        print(commit['sonarqube'])
        return None

    for file in commit['sonarqube']['files']:

        if path_in_commit == file['path']:

            return file['measures']

    newer_paths = [change['path'] for change in newer_changes]

    for file in commit['sonarqube']['files']:

        if file['path'] in newer_paths:

            print('fixed it')

            return file['measures']


def get_graph(path):

    print('Generating graph for file: {}'.format(path))

    file = db_files.find_one({'path': path})

    if file is None:
        print('File >{}< was not found. Is this its most current path?'.format(path))
        return

    dataframes = []

    for i in range(len(file['changes'])):

        change = file['changes'][i]

        res = __get_file_metrics_from_commit(change['commit_id'], change['path'], file['changes'][i:])

        if res is None:
            print('res was none')
            res = []

        res.append({'value': str(float(change['added']) - float(change['removed'])), 'metric': 'churn'})

        columns = [d['metric'] for d in res]
        data = [[d['value'] for d in res]]

        df = pd.DataFrame(data, [change['commit_id']], columns)

        dataframes.append(df)

    metrics = pd.concat(dataframes)
    metrics = metrics.reindex(sorted(metrics.columns), axis=1)

    fig = px.line(metrics, x=metrics.index, y=metrics.columns, title=path)
    fig.show()


def get_graphs(paths):

    for path in paths:
        get_graph(path)
