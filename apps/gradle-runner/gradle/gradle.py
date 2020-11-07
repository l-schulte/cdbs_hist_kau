from gradle.cli import GradleCli


def run_build(repo, project_key, token):

    cli = GradleCli()

    return cli.analyze(repo, project_key, token)
