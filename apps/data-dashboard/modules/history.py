import pymongo
import re
import progressbar

from __init__ import db_commits


def __find_file_metrics(path, files):

    for file in files:
        if file['path'] == path:
            return file['measures']


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
