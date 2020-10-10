from importer.git import git
from importer.cloc import cloc
from importer import db, db_commits, db_files

repos = list(db.repos.find())


def __store_commits(repo, commits):

    for commit in commits:
        commit['repo'] = repo['_id']

    db_commits.insert_many(commits)


def __store_changes(repo, changes):

    for change in changes:

        file = db_files.find_one({
            'path': change['old_path']
        })

        if file:
            db_files.update_one({
                '_id': file['_id']
            }, {
                '$set': {
                    'path': change['path'],
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
                'repo': repo['_id'],
                'changes': [change]
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

    for file in db_files.find({'repo': repo['_id']}):
        c_pos = 0
        for change in file['changes']:
            content = git.get_file_content(
                repo, change['commit_id'], change['path'])
            stat = cloc.analyze_file(file['path'], content)

            db_files.update_one({
                '_id': file['_id']
            }, {
                '$set': {'changes.{}.cloc'.format(c_pos): stat}
            })

            c_pos += 1


def go():
    for repo in repos:

        commits, changes = git.crawl(repo)

        __store_commits(repo, commits)
        __store_changes(repo, changes)

        __calculate_metrics(repo)
