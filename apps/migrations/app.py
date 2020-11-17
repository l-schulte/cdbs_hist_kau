from __init__ import db_commits, db_commits_backup

import progressbar

for commit_backup in progressbar.progressbar(db_commits_backup.find()):

    try:
        db_commits.update_one({'commit_id': commit_backup['commit_id']}, {
            '$set': {'sonarqube': commit_backup['sonarqube']}}, False)
    except Exception:
        print('cant find {}'.format(commit_backup['commit_id']))
