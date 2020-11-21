from flask import Flask, request
import json

from git import git
from gradle import gradle

app = Flask(__name__)


@app.route('/', methods=["POST"])
def start():

    j = request.get_json()

    if type(j) is dict:
        repo = j
    else:
        repo = json.loads(j)

    commit = request.values.get('commit', '')
    project_key = request.values.get('project_key', '')
    api_key = request.values.get('api_key', '')

    checkout = git.checkout_commit(repo, commit)

    print(checkout)

    result = gradle.run_build(repo, project_key, api_key)

    return result


@app.route('/check')
def check_running():
    return 'running', 200


if __name__ == "__main__":
    app.run(host='0.0.0.0')
