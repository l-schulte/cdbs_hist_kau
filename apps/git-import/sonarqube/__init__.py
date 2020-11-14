import os
from __init__ import db

db_sonarqube = db.sonarqube_dump

sonarqube_instance = 'http://sonarqube:9000'
gradle_runner_basename = 'cdbs_gradle-runner_{}'
workdir = os.getcwd()

API_USERNAME = 'admin'
API_PASSWORD = 'admin'

__metric_keys = [
    'ncloc',                    # Lines of code
    'statements',               # Number of statements
    'functions',                # Number of functions
    'comment_lines',            # Number of comment lines
    'comment_lines_density',    # Comment line density
    'complexity',               # Cyclomatic complexity
    'duplicated_lines',         # Number of duplicated lines
    'violations',               # Number of issues
    'code_smells',              # Number of code smells
    'bugs',                     # Number of bugs
    'vulnerabilities',          # Number of security vulnerabilities
    'sqale_index',              # Sqale index (technical debt)
    'sqale_debt_ratio'          # Sqale debt ratio
]

metric_keys = ', '.join(__metric_keys)


def print_runner(runner, message):
    print(' {} > {}'.format(runner, message))
