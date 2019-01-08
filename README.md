# Aeon #

A private monitoring API which aggregates quality issues into a simple
summary for overall health for the lifespan of an application.

[![Known Vulnerabilities](https://snyk.io/test/github/lakesite/aeon/badge.svg?targetFile=requirements.txt)](https://snyk.io/test/github/lakesite/aeon?targetFile=requirements.txt)

## Running #

  $ vagrant up

  Once running, to see a list of users:

  $ curl -H 'Accept: application/json; indent=4' -u aeon@localhost:password123 http://127.0.0.1:8000/users/

## About ##

Aeon provides an API endpoint for remote hooks to report application
and system health issues.  For example, the result of the following
can be posted daily and a summary of application health would be emailed,
sent via IRC, Slack, or IM:

  1. Production tests.
  2. System resources (disk usage).
  3. Hourly DB backups.
  4. System security, package updates.
  5. Dependency vulnerability scans.
  6. System vulnerability scans.
  7. Logging related issues.

## Running ##

    $ vagrant up

    web login: http://localhost:8000/api-auth/login/
    default router view: http://localhost:8000/

    Which should redirect to: api/v1.

## API Endpoints ##

[organization] >---< [status] --+--> [system]
                                |
                                +--> [service]     <--+
                                |                     |
                                |                     |
                                |                     |
                                +--> [application] <--+

Status event records belong to an organization, and may reference an
application, system, and/or service.  Applications should include status reports
that are central to the app itself, such as snyk or sentry reports.
Services may include logs or events from

### Organization ###

  GET|POST /organization
  json: {id, name, description}

  Required fields:
  * name: unique name for an organization.
  * description: Verbose name of organization.

### Status ###

  GET|POST /status
  json: {application_id: [key], system_id: [key], service_id: [key],
         status: [okay|warn|fail], description: '...', ...}

  Required fields:
  * application_id: key for application, for example, 'nginx'
  * system_id: key for system, for example, 'www_pool'
  * service_id: key for application component, for example, 'hourly
    backup service'.
  * status: status result of operation, which may be okay, warn, fail.
  * description: Verbose output or summary output of operation.

### System ###

    Example: www_pool (can be a collection)

    Area of concern: A system (or platform, container, etc) which runs multiple
                     user land applications and system services.

    GET|POST /system
    json: {id, organization_id, name, hostname, ip, description}

    Required fields:
    * organization_id: id for organization the system belongs to.
    * name: unique name for a system belonging to an organization.
    * ip: an ip (optional)
    * description: Verbose name of the system.

### Application ###

  Example: frontend website (php, node, etc)

  Area of concern: A specific application, which has associated OS services and
                   subsystems.

  GET|POST /application
  json: {id, name, system_id, description}

  Required fields:
  * name: unique name for an application belonging to an organization.
  * system_id: id for system the application runs on.
  * description: Verbose name of the application.

### Service ###

  Example: nginx

  Area of concern: A service which is related to, or which an application
                   depends on.  For example, the front end website depends on
                   nginx, and nginx runs on the www_pool system.

  GET|POST /service
  json: {id, name, system_id}

  Required fields:
  * name: unique name for a service belonging to a system
  * system_id:
  * description: Verbose name of the system.

## Environment Variables for Dev ##

The following environment variables can be set to configure the default superuser:

    DJANGO_DB_NAME = os.environ.get('DJANGO_DB_NAME', "aeon")
    DJANGO_SU_EMAIL = os.environ.get('DJANGO_SU_EMAIL', "aeon@localhost")
    DJANGO_SU_PASSWORD = os.environ.get('DJANGO_SU_PASSWORD', "password123")

## Requirements/Dependencies ##

  - Ubuntu 18.04, MySQL
  - Vagrant (local development)

  * Python 3.6
  * Django 2.1.2
  * DRF 3.9.0
  * Pillow 5.4.1

  The full list of requirements are provided in requirements.txt

## License ##

MIT
