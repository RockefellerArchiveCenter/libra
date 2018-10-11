# libra
A microservice to generate reports on files and activities in Fedora.

[![Build Status](https://travis-ci.org/RockefellerArchiveCenter/libra.svg?branch=master)](https://travis-ci.org/RockefellerArchiveCenter/libra)

## Installation

### Quick Start
If you have [git](https://git-scm.com/) and [Docker](https://www.docker.com/community-edition) installed:

      git clone https://github.com/RockefellerArchiveCenter/libra.git
      cd libra
      docker-compose up

To shut down Zodiac, run:

      `docker-compose down`

or, if you wish to remove all local data:

      `docker-compose down -v`


## Usage

Reports can be created and scheduled either via a user interface or HTTP POST requests (see below). At regularly scheduled intervals (or when triggered via a POST request), a cron job reviews all pending reports, and runs the reports whose `queued_time` is in the past.

![Libra process diagram](reports.png)


## Routes

A user interface which supports creating, viewing and downloading of reports is available at `/reports`.

| Method | URL | Parameters | Response  | Behavior  |
|--------|-----|---|---|---|
|POST|/fixity| |200|Creates a new fixity report|
|GET|/fixity| |200|Returns a list of fixity reports|
|GET|/fixity/{id}| |200|Returns an individual fixity report|
|DELETE|/fixity/{id}| |200|Deletes an individual fixity report|
|POST|/formats| |200|Creates a new file format report|
|GET|/formats| |200|Returns a list of file format reports|
|GET|/formats/{id}| |200|Returns an individual file format report|
|DELETE|/formats/{id}| |200|Deletes an individual file format report|
|POST|/run-reports/{report_type}| |200|Runs the reports specified by the `report_type`|
|GET|/status||200|Returns the status of the microservice|
|GET|/schema.json||200|Returns a JSON representation of the Open API schema for the service|


## License

Code is released under an MIT License, as all your code should be. See [LICENSE](LICENSE) for details.
