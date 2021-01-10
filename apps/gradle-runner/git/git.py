from git.cli import GitCli


def checkout_commit(repo, commit_id):
    """Checkout a commit from the given repository.

    If the repository does not exist locally it will be cloned automatically.

    """

    cli = GitCli(repo)

    return cli.checkout(commit_id)
