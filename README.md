# Group Web UI
A system for organizing communities, with features such as calendars,
announcements, and home pages. Currently being developed by Team C for
[CS 497S: Scalable Web Systems][1], taught by Professor Tim Richards at
UMass Amherst.

This repository contains the web user interface for this system.

The service is deployed [here][2].

## Development
To build the service for development, use the following instructions:

1. Run `./scripts/build-for-server.sh`
2. Run `pipenv install`
3. Set environment variables:
    - `export FLASK_APP=server`
    - `export FLASK_ENV=development`
    - `export GROUP_SERVER_HOST=http://<hostname>:<port>`
    - `export EVENT_SERVER_HOST=http://<hostname>:<port>`
    - `export IMAGE_SERVER_HOST=http://<hostname>:<port>`
    - If the latter three variables are not set, the server defaults to
    http://localhost:5001, http://localhost:5002, and
    http://localhost:5003, respectively.
4. Run `pipenv run flask run`

The build-for-server script must be re-run each time the client is
edited in order for Flask to serve it. Alternatively, `cd` into
[client](client) and run `yarn serve` to refresh the client after each
change. This method does not allow the client to connect to the server.

## Design and Implementation
This web app is designed according to the backends for frontends
pattern described by Sam Newman in *Building Microservices*. The server
sends a single-page [Vue.js](https://vuejs.org/) app and also hosts an
API to service requests from the client.

The server is developed with [Flask](https://flask.palletsprojects.com/)
and uses the [Requests](https://requests.readthedocs.io/) library to
send requests to upstream services. The data from the responses is then
repackaged and sent along to the client. In this way, the backend can
organize data in a more convenient format for the client.

## API
Documentation for the backend's API is [here](server/README.md).

[1]: https://sites.google.com/cs.umass.edu/compsci-497s-f20-submissions
[2]: http://groupwebui-env.eba-9tq2awwf.us-east-1.elasticbeanstalk.com/
