# Aeon #

A private monitoring API which aggregates quality issues into a simple
summary for overall health for the lifespan of an application.

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

## API Endpoints ##

  * POST /status
  json: {application_id: [key], service: [key], status: [okay|warn|fail], 
         description: '...', ...}

  Required fields:
  * application_id: key for application.  Multiple applications or systems 
    may fall under one client.
  * service: key for application componant, for example, 'hourly 
    backup service'.
  * status: status result of operation, which may be okay, warn, fail.
  * description: Verbose output or summary output of operation.

  Optional fields:


## License ##

MIT
