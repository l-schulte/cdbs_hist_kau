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

            print('fixed it {}'.format(commit['date']))

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

        res_dict = {}

        for item in res:
            res_dict[item['metric']] = item['value']

        res_dict['churn'] = str(float(change['added']) - float(change['removed']))
        res_dict['date'] = str(change['date'])
        res_dict['path'] = path
        res_dict['color'] = input['color']
        res_dict['counter'] = str(i - change_count)
        res_dict['commit_id'] = change['commit_id']

        df = pd.DataFrame(res_dict, [i - change_count])
        dataframes.append(df)

    metrics = pd.concat(dataframes)

    return metrics


def get_graphs_per_file(files):

    relevant_metrics = [m.value for m in [Metric.NCLOC, Metric.FUNCTIONS, Metric.SQALE_INDEX]]

    for file in files:

        df = get_dataframes(file)

        fig = px.line(df, x='counter', y=relevant_metrics, title=file['path'])
        fig.show()


def get_graphs_per_metric(files, draw=True):

    metrics = None

    for i, file in files.iterrows():

        metric = get_dataframes(file)

        if metrics is None:
            metrics = metric
        else:
            metrics = metrics.append(metric)

    relevant_metrics = [Metric.NCLOC, Metric.FUNCTIONS, Metric.SQALE_INDEX, Metric.CHURN,
                        Metric.COMMENT_LINES, Metric.COMMENT_LINES_DENSITY,
                        Metric.COMPLEXITY, Metric.SQALE_DEBT_RATIO, Metric.STATEMENTS]

    if not draw:
        return metrics

    for key in relevant_metrics:

        fig = px.line(metrics, x='counter', y=key.value, title=key.value, color='path', line_group='path')
        fig.show()
