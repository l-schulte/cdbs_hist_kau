import progressbar
import pymongo
import threading
from time import sleep
from __init__ import db, db_commits, db_files
from git import git
from sonarqube import sonarqube

repos = list(db.repos.find())


def __store_commits(repo, commits):

    print('-> commits')

    for commit in progressbar.progressbar(commits):
        commit['repo'] = repo['_id']

    db_commits.insert_many(commits)


def __store_changes(repo, changes):

    print('-> changes')

    for change in progressbar.progressbar(changes):

        file = db_files.find_one({
            'path': change['old_path']
        })

        if file:
            db_files.update_one({
                '_id': file['_id']
            }, {
                '$set': {
                    'path': change['path'],
                    'repo': repo['_id'],
                    'changes': {
                        change['commit_id']: change
                    }
                }
            }, True)

            file_id = file['_id']
        else:
            res = db_files.insert_one({
                'path': change['path'],
                'repo': repo['_id'],
                'changes': {
                    change['commit_id']: change
                }
            })

            file_id = res.inserted_id

        db_commits.update_one({
            'commit_id': change['commit_id']
        }, {
            '$push': {
                'files': file_id
            }
        })


def __calculate_metrics(repo):

    # for file in db_files.find({'repo': repo['_id']}):
    #     for id in file['changes']:
    #         change = file['changes'][id]
    #         content = git.get_file_content(
    #             repo, change['commit_id'], change['path'])
    #         stat = cloc.analyze_file(file['path'], content)

    #         db_files.update_one({
    #             '_id': file['_id']
    #         }, {
    #             '$set': {'changes.{}.cloc'.format(id): stat}
    #         })

    for commit in db_commits.find({'repo': repo['_id'], 'sonarqube.status': {'$in': [False, None]}})\
            .sort('date', pymongo.DESCENDING).batch_size(10):

        print('Next in queue: {} - {}'.format(commit['commit_id'][:6], commit['date']))

        runner = None
        while runner is None:
            runner = sonarqube.get_runner()
            sleep(15)

        print('Running {}'.format(commit['commit_id'][:6]))

        th = threading.Thread(target=__run_threaded_sonarqube, args=(commit, runner, repo))
        th.start()


def __run_threaded_sonarqube(commit, runner, repo):

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

    for repo in repos:

        # print('Crawling...')
        # commits, changes = git.crawl(repo)

        # print('Saving...')
        # __store_commits(repo, commits)
        # __store_changes(repo, changes)

        print('Calculating...')
        __calculate_metrics(repo)

        print('Done')


print('GO')
go()
