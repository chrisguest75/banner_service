# README

## TODO
1) Fix up the interface to handle parameters
1) Add metrics
1) Add opentelemetry.  
1) Try out as a lambda service.
1) APi gateway. 
1) skaffold with kind for local debugging
1) datadog metrics? 

## Prerequisites

Configure the following tools:

1. [Pyenv](https://github.com/pyenv/pyenv)
1. [Intro to Pyenv](https://realpython.com/intro-to-pyenv/)
1. [Pipenv](https://realpython.com/pipenv-guide/)

## Installation

To install the service locally.

```sh
git clone <repo>
cd <repo>
export PIPENV_VENV_IN_PROJECT=1
pipenv install --three
```

## Start

Start the Flask App

```sh
python ./main.py
```
## Docker image
```sh
# build image
docker build -t banner_service .
docker run --rm -e COLUMNS=${COLUMNS} -e TERM=${TERM} -e PORT=5000 -p 5000:5000 banner_service

echo $(curl -s -X GET --header 'Accept: application/json' 'http://localhost:5000/api/banner?message=whatever&fontname=cuddly')
echo $(curl -s -X GET --header 'Accept: application/json' 'http://localhost:5000/api/banner?message=whatever&fontname=knight4')
echo $(curl -s -X GET --header 'Accept: application/json' 'http://localhost:5000/api/banner?message=whatever&fontname=tcb')
echo $(curl -s -X GET --header 'Accept: application/json' 'http://localhost:5000/api/banner?message=whatever&fontname=carebear')

```

