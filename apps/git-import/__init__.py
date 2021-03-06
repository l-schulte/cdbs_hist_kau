from pymongo import MongoClient

MONGODB_ADDR = 'mongodb'

client = MongoClient('mongodb://%s:%s@%s' %
                     ('root', 'localdontuseglobal', MONGODB_ADDR))

db = client.cdbs_db
db_log = db.import_log
db_commits = db.commits
db_files = db.files

db_commits.create_index('date')


def b2s(byte):
    """Converts bytes to string.

    Used throughout the tool in combination with return values from subprocess.run()

    """
    return '' if not byte else byte.decode("utf-8")
