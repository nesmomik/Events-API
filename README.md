### course topic: from API to a production ready cloud service.

repository: [GitHub](https://github.com/nesmomik/Events-API)

more documentation of the Events-API at the upstream repository:  [GitHub](https://github.com/Masterschool-SWE/Events-API)

## course topic: from API to a production ready cloud service.

repository: [GitHub](https://github.com/nesmomik/Events-API)

### part 1: discover the API / preparation
Overview:
- the [OpenAPI Specification](https://learn.openapis.org/), is a specification for a machine-readable interface definition language for describing, producing, consuming and visualizing web services
- in the project a `openapi.yaml` file is provided to document the API
- this allows to use [SwaggerUI](https://swagger.io/tools/swagger-ui/) to explore the API functionality and also to try it out

Completed Tasks:
- forked the upstream repo
- set up the environment with `uv`
- run and explore the repo


### part 2: test the API
Overview:
- use the [pytest](https://docs.pytest.org/en/stable/) framework
- create unit tests
- create integration test
file structure:
```
├── /test
│   ├── __init__.py         # define package (namespacing) 
│   ├── conftest.py         # shared fixtures (dependency injection)
│   ├── test_api.py         # integration testing
│   └── test_models.py      # unit testing
```
 
Completed Tasks:
- created Makefile to run tests
Notes:
- basics of [Testing Flask Applications](https://flask.palletsprojects.com/en/stable/testing/)
- learned about the difference between
    - unit tests
    - integration tests
    - end-to-end test
  so i adjusted the file structure accordingly to incorporate a seperate directory for the e2e tests
```
├── tests/
│   ├── conftest.py          <-- Global fixtures (like the DB setup)
│   ├── unit/                <-- Low-level logic (test_models.py)
│   │   └── test_password_hashing.py
│   ├── integration/         <-- The 'client' fixture (test_api.py)
│   │   └── test_events_flow.py
│   └── e2e/                 <-- The 'requests' library
│       ├── conftest.py      <-- E2E specific setup (starting the server)
│       └── test_system.py
```
- use fixtures to make the tests environment agnostic
- unit tests are cheap and fast
- integration tests are more expensive
- dependency injection ensures:
    - inversion of control
    - decoupling
    - mockability
- dependency injection mitigates the dependency by injecting data/objects like:
    - time
    - external APIs
    - environment variables and secrets
    - file system
    - databases
- parametrization of test implements DRY (don't repeat yourself)
