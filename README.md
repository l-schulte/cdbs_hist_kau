# Get started

[Project report - PDF](/resources/Research%20Project%20in%20Computer%20Science%20-%20Analyzing%20Dependencies%20between%20Software%20Architectural%20Degradation%20and%20Code%20Complexity%20Trends.pdf)

## Requirements

- Execution environment requirements:
  - Docker
- Requirements for analyzed project:
  - Hosted on a git repository accessible to the machine
  - Java project with Gradle wrapper (when using SonarQube)

## Setup

1. Clone the master branch of this repository
2. Start MongoDB Docker instance for initial configuration:
   - `docker-compose create`
   - `docker-compose start mongodb`
3. Connect to MongoDB shell in Docker container:
   - `docker exec -it mongodb mongo --username "root" --password "localdontuseglobal"`
4. Insert repository information for project that is to be analyzed:
   - `use cdbs_db`
   - ` db.repos.insert( { title: "jabref", url: "https://github.com/JabRef/jabref.git", start: "fd695d24782266018ee90407cf1210959c238bb2", end: "2014-07-13" } )`

# Tool design

## Building blocks

![](/resources/class_diagram.png)

## Communication context

![](/resources/business_context.png)

## Deployment context

![](/resources/deployment.png)
