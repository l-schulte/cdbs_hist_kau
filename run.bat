@echo off
set /p gradle_runner="Enter number of gradle runners to start: "
@echo on

docker-compose up --scale gradle-runner=%gradle_runner% --build -d
docker attach git-importer