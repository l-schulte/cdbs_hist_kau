from pymongo import MongoClient

client = MongoClient('mongodb://%s:%s@127.0.0.1' %
                     ('root', 'localdontuseglobal'))

db = client.cdbs_db
db_log = db.import_log
db_commits = db.commits
db_files = db.files
