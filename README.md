# Brite MDB
An API to manage a collection of movies

deployed at;
https://britemdb-dkckvyosiq-ue.a.run.app

user credentials to use delete api;
user1
passwd1

# SETUP AND RUN

edit .env with appropriate values if needed, current values have my secrets for convenience and should run ok
cp sample.env .env

## to run on gcp
cp sample.env .env
./init_gcp.sh

## to run locally
cp sample.env .env
docker compose up
- open http://localhost/

## run tests
- install firebase tools; for example for Linux or Mac;
curl -sL https://firebase.tools | bash
- install poetry

- install dependencies
poetry shell
poetry install

- run local tests
cp sample.env .env
firebase --only firestore emulators:exec "poetry run pytest tests/endpoints"

##  Description

- api is developed with FastAPI, provides openapi.json and swagger ui as well
- api deploys to cloud run
- store data on firestore backend, emulated locally for local run and tests

This is a basic python api setup using the FastAPI framework. It is deployable to the Google Cloud.


## Based on FastApi Poetry Template from github.com:zdmwi/fastapi-starter-template

###  Directory Structure
```
fastapi-starter-template
├── app
│   ├── api
│   │   ├── endpoints
│   │   │   ├── __init__.py
│   │   │   └── hello.py
│   │   └── __init__.py
│   ├── core
│   │   ├── __init__.py
│   │   └── application.py
│   ├── __init__.py
│   └── main.py
├── tests
│   ├── endpoints
│   │   └── hello_test.py
│   ├── __init__.py
│   └── conftest.py
├── Dockerfile
├── README.md
├── docker-compose.yaml
├── poetry.lock
├── pyproject.toml
└── tox.ini
```

###  Features

-  Logging

-  Testing & Coverage

-  REST API support

-  Automatic API documentation

-  Pre-Commit Code Linting & Formatting

##  Getting Started

Getting started developing with this template is pretty simple using docker and docker-compose.

```shell script
# Clone the repository
git clone git@github.com:zdmwi/fastapi-starter-template.git

# cd into project root
cd fastapi-starter-template

# Launch the project
docker-compose up
```

Afterwards, the project will be live at [http://localhost:5000](http://localhost:8000).

## Documentation

FastAPI automatically generates documentation based on the specification of the endpoints you have written. You can find the docs at [http://localhost:8000/docs](http://localhost:5000/docs).

## Testing

In order to test and lint the project locally you need to install the poetry dependencies outlined in the pyproject.toml file.

If you have Poetry installed then it's as easy as running `poetry shell` to activate the virtual environment first and then `poetry install` to get all the dependencies.

This starter template has an example test which covers its only endpoint. To run the test, ensure you are
in the same directory as the `tox.ini` file and run `tox` from the command line. It will also perform code
linting and formatting as long as the pre-commit hooks were installed. We'll talk about that next.

# Code Formatting & Linting

To activate pre-commit formatting and linting all you need to do is run `pre-commit install` from the root of your local git repository. Now
every time you try to make a commit, the code will be formatted and linted for errors first.
