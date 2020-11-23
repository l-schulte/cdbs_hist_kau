import plotly.express as px
import pandas as pd
import pymongo

from __init__ import db_commits, db_files, Metric


def __get_file_metrics_from_commit(commit_id, path_in_commit, newer_changes):

    commit = db_commits.find_one({'commit_id': commit_id})

    if commit is None\
            or 'sonarqube' not in commit\
            or 'status' not in commit['sonarqube']\
            or commit['sonarqube']['status'] is not True:

        commit = db_commits.find_one({'date': {'$gte': commit['date']}, 'sonarqube.status': True}, sort=[
                                     ('date', pymongo.ASCENDING)])

    if commit is None or commit['sonarqube']['status'] == 'Error':
        print(commit_id)
        return None

    for file in commit['sonarqube']['files']:

        if path_in_commit == file['path']:

            return file['measures']

    newer_paths = [change['path'] for change in newer_changes]

    for file in commit['sonarqube']['files']:

        if file['path'] in newer_paths:

            # print('fixed it')

            return file['measures']


def get_dataframes(input):

    path = input['path']

    print('Generating graph for file: {}'.format(path))

    file = db_files.find_one({'path': path})

    if file is None:
        print('File >{}< was not found. Is this its most current path?'.format(path))
        return

    dataframes = []
    changes = sorted(file['changes'], key=lambda x: x['date'])
    change_count = len(file['changes'])

    for i in range(len(changes)):

        change = changes[i]

        res = __get_file_metrics_from_commit(change['commit_id'], change['path'], file['changes'][i:])

        if res is None:
            print('res was none')
            res = []

        res.append({'value': str(float(change['added']) - float(change['removed'])), 'metric': 'churn'})
        res.append({'value': str(change['date']), 'metric': 'date'})
        res.append({'value': path, 'metric': 'path'})
        res.append({'value': input['good'], 'metric': 'good'})
        res.append({'value': str(i - change_count), 'metric': 'counter'})
        res.append({'value': change['commit_id'], 'metric': 'commit_id'})

        columns = [d['metric'] for d in res]
        data = [d['value'] for d in res]

        df = pd.DataFrame([data], ['{} - {}'.format(change['commit_id'], path)], columns)

        dataframes.append(df)

    metrics = pd.concat(dataframes)
    # metrics = metrics.reindex(sorted(metrics.columns), axis=1)

    return metrics


def get_graphs_per_file(files):

    for file in files:

        metrics = get_dataframes(file)

        relevant_metrics = [m.value for m in [Metric.NCLOC, Metric.FUNCTIONS, Metric.SQALE_INDEX]]

        fig = px.line(metrics, x='counter', y=relevant_metrics, title=file['path'])
        fig.show()


def get_graphs_per_metric(files):

    metrics = None

    for file in files:

        metric = get_dataframes(file)

        if metrics is None:
            metrics = metric
        else:
            metrics = metrics.append(metric)

    relevant_metrics = [Metric.NCLOC, Metric.FUNCTIONS, Metric.SQALE_INDEX, Metric.CHURN]

    for key in relevant_metrics:

        fig = px.line(metrics, x='date', y=key.value, title=key.value, color='good', line_group='path')
        fig.show()
