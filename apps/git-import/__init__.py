from pymongo import MongoClient

MONGODB_ADDR = 'mongodb'

client = MongoClient('mongodb://%s:%s@%s' %
                     ('root', 'localdontuseglobal', MONGODB_ADDR))

db = client.cdbs_db
db_log = db.import_log
db_commits = db.commits
db_files = db.files
