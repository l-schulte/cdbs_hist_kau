from git.cli import GitCli


def checkout_commit(target, commit_id):

    cli = GitCli(target)

    return cli.checkout(commit_id)
