# Events API: eductional repository
## Course topic: From API to a production ready cloud service.

More documentation of the Events-API at the upstream repository:  [GitHub](https://github.com/Masterschool-SWE/Events-API)


## Part 1: Discover the API / Preparation

Goal: Run the Events-API and explore it with the docs and an API tool like Postman. 

Completed Tasks:
- forked the upstream repo
- made the project managed by [uv](https://docs.astral.sh/uv/)
- run and explore the repo

Notes:
- the [OpenAPI Specification](https://learn.openapis.org/), is a specification for a machine-readable interface definition language for describing, producing, consuming and visualizing web services
- in the project a `openapi.yaml` file is provided to document the API
- this allows to use [SwaggerUI](https://swagger.io/tools/swagger-ui/) to explore the API functionality and also to try it out

Commands:
```
# create pyproject.toml
uv init --bare

# add dependencies
uv add -r requirements.txt

# run app
uv run app.py

# test health endpoint
curl -sf http://localhost:5000/api/health
```

## Part 2: Test the API

Goal: Add a basic automated test suite for the Events-API.

Overview:
- use the [pytest](https://docs.pytest.org/en/stable/) framework
- create unit tests
- create integration tests
 
Completed Tasks:
- created unit test
- created integration tests
- created end-to-end tests
- created Makefile to run tests

Notes:
- basics of [Testing Flask Applications](https://flask.palletsprojects.com/en/stable/testing/)
- learned about the difference between
    - unit tests
    - integration tests
    - end-to-end test
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

Commands:
```
# show all commands
make help   

# run all tests
make test
```

## Part 3: Containerization

Goal: Package the Events API in a Docker container and verify the tests pass.

Overview:
- create Dockerfile
- build container
- run tests against container

Completed tasks:
- added Dockerfile and .dockerignore
- build and run container
- copied end-to-end tests and changed fixture to be able to use them with the container

Notes:
- can use a two stage container build, when using uv for dependencies
- setting PYTHONPATH in pyproject.toml simplifies module importing and test execution

Commands:
```
# build Docker image
docker build -t events-api:test .

# start container
docker run -d -p 5000:5000 --name events-api-test events-api:test

# run container tests
make test-container
```


## Part 4: Continous Integration

Goal: Add a basic CI pipeline to the Events API GitHub repository using GitHub Actions.

Overview:
- use github actions to automate testing
- push or pull-requests trigger:
    - container build of the source code 
    - run container
    - run pytest vs containerized app

Completed tasks:
- setup initial github action workflow
- added unit and integration tests job
- setup initial container build and run job
- added container tests and cleanup step
- added `workflow_dispatch` event trigger to allow manual run on [GitHub](https://github.com/nesmomik/Events-API/actions/workflows/ci.yml)

Notes:
- a specific workflow can be run on all branches or on specific branches only
- not all actions are in [Actions](https://github.com/actions), but most are in the [Marketplace](https://github.com/marketplace)
- bash scripts allowed in steps

Commands:
```
# force empty commit
git commit --allow-empty -m "chore: trigger CI"

# trigger workflow
git push
```

## Part 5: Continuous Deployment

Goal: Deploy your Events API to the cloud using Docker Hub and Render and test it

Completed Tasks:
- build and push image to [Docker Hub](https://hub.docker.com/repositories/nesmomik)
- create [Render](https://render.com/) [webservice](https://events-api-lt80.onrender.com/apidocs/)
- create GitHub environment to manage environment variables and secrets in GitHub Actions
- create new render-deployment job in the GitHub Actions workflow

Commands:
```
# log in to docker account (nesmomik)
docker login

# build Docker image with account name
docker build -t nesmomik/events-api .

# push the image to docker hub
docker push

# trigger the deploy webhook
curl <secret-webhook-url>
```

Notes:
- Register on Render with GitHub from the start automatically allows GitOps workflow
