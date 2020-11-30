import pandas as pd
import pymongo
import csv
import progressbar

from data import db_commits, db_files


def __get_file_metrics_from_commit(commit_id, newer_changes):

    commit = db_commits.find_one({'commit_id': commit_id})

    if commit is not None and\
        ('sonarqube' not in commit or
         'status' not in commit['sonarqube'] or
         commit['sonarqube']['status'] is not True):

        commit = db_commits.find_one({'date': {'$gte': commit['date']}, 'sonarqube.status': True}, sort=[
                                     ('date', pymongo.ASCENDING)])

    if commit is None or commit['sonarqube']['status'] == 'Error':
        print(commit_id)
        return None

    newer_paths = [change['path'] for change in newer_changes]

    for file in commit['sonarqube']['files']:

        if file['path'] in newer_paths:

            return file['measures']


def __get_dataframes_for_file(input):

    path = input['path']

    file = db_files.find_one({'path': path})

    if file is None:
        print('File >{}< was not found. Is this its most current path?'.format(path))
        return

    dataframes = []
    changes = sorted(file['changes'], key=lambda x: x['date'])
    change_count = len(file['changes'])

    for i in range(len(changes)):

        change = changes[i]

        res = __get_file_metrics_from_commit(
            change['commit_id'], file['changes'][i:])

        if res is None:
            res = []

        res.append({'value': float(change['added']) - float(change['removed']), 'metric': 'churn'})
        res.append({'value': change['date'].timestamp(), 'metric': 'date'})
        res.append({'value': path, 'metric': 'path'})
        res.append({'value': input['good'], 'metric': 'good'})
        res.append({'value': i - change_count, 'metric': 'counter'})
        res.append({'value': change['commit_id'], 'metric': 'commit_id'})

        columns = [d['metric'] for d in res]
        data = [d['value'] for d in res]

        df = pd.DataFrame(
            [data], None, columns)

        dataframes.append(df)

    metrics = pd.concat(dataframes)

    return metrics


def __get_paths_from_filenames(class_file_data):

    for cf in class_file_data:

        file = db_files.find_one({'path': {'$regex': '/{}.java'.format(cf['file'])}},
                                 sort=[('changes.length', pymongo.DESCENDING)])

        cf['path'] = file['path']

    return class_file_data


def __read_class_file_tuple():

    class_file_data = []

    with open('data/class-file.csv') as csv_file:

        csv_reader = csv.reader(csv_file, delimiter='\t')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                class_file_data.append({'file': row[0], 'good': row[1] == 'TRUE'})

        print(f'Processed {line_count} lines.')

    return class_file_data


def store_data():

    class_file_data = __read_class_file_tuple()

    class_path_data = __get_paths_from_filenames(class_file_data)

    df = pd.DataFrame(class_path_data)
    df.to_csv('data/class-path.csv', sep='\t')

    dataframes = []

    for file in progressbar.progressbar(class_path_data):

        df = __get_dataframes_for_file(file)

        dataframes.append(df)

    df = pd.concat(dataframes)
    df.to_csv('data/file-metrics.csv', sep='\t')
