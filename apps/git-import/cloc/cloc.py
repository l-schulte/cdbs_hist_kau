
import tempfile
from cloc.cli import ClocCli


def analyze_file(path, content):
    cli = ClocCli()

    name = path.rsplit('/', 1)[-1]

    tmpdir = tempfile.TemporaryDirectory(prefix='cdbs_')

    tmp = open('{}\\{}'.format(tmpdir.name, name), 'w')
    tmp.write(content)
    tmp.close()

    stat = cli.get_stat(tmp, content)

    tmpdir.cleanup()

    code = stat['SUM']['code']
    comment = stat['SUM']['comment']
    blank = stat['SUM']['blank']
    lines = code + comment + blank

    return {'lines': lines, 'code': code, 'comment': comment, 'blank': blank}
