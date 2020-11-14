import subprocess
import os
import time

from gradle import sonarqube_instance, workdir, sonarqube_plugin_id, sonarqube_plugin_apply, sonarqube_plugin_classpath


def b2s(byte):
    return '' if not byte else byte.decode("utf-8")


class GradleCli:

    def __add_sonarqube_to_gradle(self):
        build_file = open("build.gradle", "r")
        content = build_file.read()
        build_file.close()

        if 'sonarqube' not in content:
            lines = content.splitlines()

            if 'plugins {' in content:
                # Version using Gradle’s DSL languages
                for i in range(len(lines)):
                    if lines[i].startswith('plugins {'):
                        lines.insert(i+1, '    ' + sonarqube_plugin_id)
                        break

                for i in range(len(lines)):
                    if 'net.ltgt.errorprone' in lines[i]:
                        lines[i] = '    '

            else:
                # Version using legacy plugin
                for i in range(len(lines)):
                    if lines[i].startswith('    dependencies {'):
                        lines.insert(i+1, '        ' + sonarqube_plugin_classpath)
                        lines.append(sonarqube_plugin_apply)

            build_file = open("build.gradle", "w")
            build_file.write('\n'.join(lines))
            build_file.close()

    def __gradle_download_https(self):
        path = "gradle/wrapper/gradle-wrapper.properties"

        if not os.path.isfile(path):
            return

        gradle_props = open(path, "r")
        content = gradle_props.read()
        gradle_props.close()

        content = content.replace('http\\:', 'https\\:')

        gradle_props = open(path, "w")
        gradle_props.write(content)
        gradle_props.close()

    def __modify_gradle(self):
        self.__add_sonarqube_to_gradle()
        self.__gradle_download_https()

    def analyze(self, repo, project_key, token):

        os.chdir('repos/{}'.format(repo['title']))

        if not os.path.isfile('build.gradle'):
            return 'Missing build.gradle', 500

        self.__modify_gradle()

        command = './gradlew -x test testClasses sonarqube ' + \
            '-D file.encoding=UTF-8 '\
            '-D sonar.projectKey={} -D sonar.host.url={} -D sonar.login={}'\
            .format(project_key, sonarqube_instance, token)

        start_time = time.time()

        res = subprocess.run(command, capture_output=True, shell=True)

        os.chdir(workdir)

        if not res.returncode == 0:
            print(b2s(res.stderr))
            return b2s(res.stderr), 500

        return str(start_time), 200
