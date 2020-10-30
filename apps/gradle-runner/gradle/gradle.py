from gradle.cli import GradleCli


def run_build(project, project_key, token):

    cli = GradleCli()

    return cli.analyze(project, project_key, token)
