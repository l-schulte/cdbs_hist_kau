from pymongo import MongoClient

client = MongoClient('mongodb://%s:%s@%s' %
                     ('root', 'localdontuseglobal', 'localhost'))

db = client.cdbs_db
db_log = db.import_log
db_commits = db.commits
db_files = db.files
