from git.cli import GitCli


def checkout_commit(repo, commit_id):

    cli = GitCli(repo)

    return cli.checkout(commit_id)
