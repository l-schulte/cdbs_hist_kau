from pymongo import MongoClient

MONGODB_ADDR = 'mongodb'

client = MongoClient('mongodb://%s:%s@%s' %
                     ('root', 'localdontuseglobal', MONGODB_ADDR))

db = client.cdbs_db
db_commits = db.commits
db_files = db.files

ARCHITECTURE_FILE = 'jabref-archmodel.txt'
