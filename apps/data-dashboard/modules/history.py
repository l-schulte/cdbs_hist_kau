import pymongo
import re
import progressbar

from __init__ import db_commits, db_files


def __find_file_metrics(path, files):

    for file in files:
        if file['path'] == path:
            return file['measures']


def __regex_check_paths(regex, file):

    path = file['path'].replace('/', '.')
    if re.search(regex, path):
        return True

    f = db_files.find_one({'_id': file['id']})

    if f is None:
        print(file)

    for change in f['changes']:

        if change['path'] != change['old_path'] and re.search(regex, change['path']):
            return True


def get_metrics(module):

    metrics_sum = {}

    for commit in progressbar.progressbar(db_commits.find({'sonarqube.status': True})
                                          .sort('date', pymongo.DESCENDING)):

        if 'files' not in commit:
            print('\nfiles not in commit:')
            print(commit['commit_id'])
            continue

        for file in commit['files']:

            path = file['path'].replace('/', '.')
            for regex in module:

                if re.search(regex, path):

                    metrics = __find_file_metrics(file['path'], commit['sonarqube']['files'])

                    if metrics is None:
                        print('\nmetrics is none')
                        print(commit['commit_id'])
                        print(path)
                        continue

                    for value in metrics:

                        if value['metric'] in metrics_sum:
                            metrics_sum[value['metric']] += float(value['value'])
                        else:
                            metrics_sum[value['metric']] = float(value['value'])

    return metrics_sum


def get_metrics_per_day(module):

    metrics_per_day = {}

    for commit in progressbar.progressbar(db_commits.find({'sonarqube.status': True})
                                          .sort('date', pymongo.DESCENDING)):

        day = commit['date'].date().isoformat()

        if 'files' not in commit:
            continue

        for file in commit['sonarqube']['files']:

            for regex in module:

                if __regex_check_paths(regex, file):

                    metrics = file['measures']

                    if metrics is None:
                        continue

                    if 'file_count' not in metrics_per_day:
                        metrics_per_day['file_count'] = {}

                    if day not in metrics_per_day['file_count']:
                        metrics_per_day['file_count'][day] = {
                            'value': 0,
                            'count': 0
                        }

                    metrics_per_day['file_count'][day]['value'] += 1
                    metrics_per_day['file_count'][day]['count'] += 1

                    for metric in metrics:

                        if metric['metric'] not in metrics_per_day:
                            metrics_per_day[metric['metric']] = {}

                        if day not in metrics_per_day[metric['metric']]:
                            metrics_per_day[metric['metric']][day] = {
                                'value': 0,
                                'count': 0
                            }

                        if day in metrics_per_day[metric['metric']] and float(metric['value']) != 0:
                            metrics_per_day[metric['metric']][day]['value'] += float(metric['value'])
                            metrics_per_day[metric['metric']][day]['count'] += 1

    return metrics_per_day
