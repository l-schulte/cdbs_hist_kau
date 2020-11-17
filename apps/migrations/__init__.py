from pymongo import MongoClient

MONGODB_ADDR = 'localhost'

client = MongoClient('mongodb://%s:%s@%s' %
                     ('root', 'localdontuseglobal', MONGODB_ADDR))

db = client.cdbs_db
db_commits = db.commits
db_commits_backup = db.commits_backup_17_11
db_files = db.files
