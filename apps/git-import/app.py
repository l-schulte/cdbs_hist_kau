import progressbar
import pymongo
import threading
from time import sleep
from __init__ import db, db_commits, db_files
from git import git
from sonarqube import sonarqube

repos = list(db.repos.find())


def __store_commits(repo, commits):
    """Stores commits found in repository.

    """

    print('-> commits')

    for commit in progressbar.progressbar(commits):
        commit['repo'] = repo['_id']

    db_commits.insert_many(commits)


def __store_changes(repo, changes):
    """Stores changes found in repository.

    """

    print('-> changes')

    for change in progressbar.progressbar(changes):

        file = db_files.find_one({
            'tmp_path': change['path']
        })

        if file:
            db_files.update_one({
                '_id': file['_id']
            }, {
                '$set': {
                    'tmp_path': change['old_path'],
                    'repo': repo['_id']
                },
                '$push': {
                    'changes': change
                }
            }, True)

            file_id = file['_id']
        else:
            res = db_files.insert_one({
                'path': change['path'],
                'tmp_path': change['old_path'],
                'repo': repo['_id'],
                'changes': [change]
            })

            file_id = res.inserted_id

        db_commits.update_one({
            'commit_id': change['commit_id']
        }, {
            '$push': {
                'files': {
                    'id': file_id,
                    'path': change['path']
                }
            }
        })


def __calculate_metrics(repo):
    """Initializes (asynchronous) calculation and storage of metrics.

    Start here when integrating new metric sources.

    Current metric sources integrated:
     - SonarQube (via Gradle runner)

    """

    for commit in db_commits.find({'repo': repo['_id'], 'sonarqube.status': {'$in': [False, None]}})\
            .sort('date', pymongo.ASCENDING).batch_size(1):

        print('Next in queue: {} - {}'.format(commit['commit_id'][:6], commit['date']))

        runner = None
        while runner is None:
            runner = sonarqube.get_runner()
            sleep(15)

        print('Running {}'.format(commit['commit_id'][:6]))

        th = threading.Thread(target=__run_threaded_sonarqube, args=(commit, runner, repo))
        th.start()


def __run_threaded_sonarqube(commit, runner, repo):
    """Thread handeling sonarqube analysis via gradle runner.

    Starts analysis on free runner and waits for results, writing them into the database.

    """

    request, response = sonarqube.start_analysis(commit, runner, repo)

    if not request.ok:
        print('{} - Analysis ran into an error: {}'.format(runner, response))
        db_commits.update_one({'_id': commit['_id']}, {'$set': {'sonarqube': {'error': response, 'status': False}}})
        return

    start_time = float(response)

    sonarqube_data = sonarqube.read_analysis(start_time, runner)

    print('{} - writing data'.format(runner))

    db_commits.update_one({'_id': commit['_id']}, {'$set': {'sonarqube': sonarqube_data}})


def go():
    """Go trough import steps: crawling, saving, calculating

    Steps can be skipped by out-commenting the corresponding lines here.

    """

    for repo in repos:

        print('Crawling...')
        commits, changes = git.crawl(repo)

        print('Saving...')
        __store_commits(repo, commits)
        __store_changes(repo, changes)

        print('Calculating...')
        __calculate_metrics(repo)

        print('Done')


print('GO')
go()
