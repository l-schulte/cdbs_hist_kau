from importer.sonarqube import sonarqube
from importer.git import git
from importer.cloc import cloc
from importer import db, db_commits, db_files
import progressbar

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

    for commit in progressbar.progressbar(db_commits.find({'repo': repo['_id']})):

        if 'sonarqube' in commit:
            continue

        # git.checkout_commit(repo, commit['commit_id'])
        sonarqube_data = sonarqube.analyze(commit)

        return

        # db_commits.update_one({'_id': commit['_id']}, {'$set': {'sonarqube': sonarqube_data}})


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
