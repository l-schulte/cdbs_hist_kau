import os

sonarqube_instance = 'http://sonarqube:9000'
workdir = os.getcwd()

sonarqube_plugin_id = 'id "org.sonarqube" version "2.7"'
sonarqube_plugin_classpath = 'classpath "org.sonarsource.scanner.gradle:sonarqube-gradle-plugin:2.7"'
sonarqube_plugin_apply = 'apply plugin: "org.sonarqube"'
