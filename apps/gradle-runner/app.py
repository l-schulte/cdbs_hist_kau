from flask import Flask, request

import git
import gradle

app = Flask(__name__)


@app.route('/')
def start():

    target = request.args.get('target', '')
    commit = request.args.get('commit', '')
    project_key = request.args.get('project_key', '')
    api_key = request.args.get('api_key', '')

    git.checkout_commit(target, commit)

    start_time = gradle.run_build(target, project_key, api_key)

    return start_time


if __name__ == "__main__":
    app.run()
