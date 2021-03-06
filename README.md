# README

## TODO
1) non-docker build is not working
1) swagger interface not working
1) add tests
1) Landing page
1) Add custom metrics
1) Add opentelemetry.  
1) datadog metrics? 
1) Try out as a lambda service.
1) APi gateway. 
1) Add kind deployment 
1) skaffold with kind for local debugging
1) prometheus and grafana.

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
pipenv shell
python ./main.py
```

## Docker image
Build, run and test
```sh
# build image and run 
docker build -t banner_service .
docker run --rm -e COLUMNS=${COLUMNS} -e TERM=${TERM} -e PORT=5000 -p 5000:5000 banner_service

open http://localhost:5000/
curl http://localhost:5000/favicon.ico

# test api ui
open http://localhost:5000/api/ui

# test metrics
curl http://localhost:5000/metrics

# test endpoints
curl http://localhost:5000/api/fonts
curl http://localhost:5000/api/health
curl http://localhost:5000/api/ready

# get banners
curl -s -X GET "http://localhost:5000/api/banner?message=whatever&fontname=cuddly&width=165"
curl -s -X GET "http://localhost:5000/api/banner?message=whatever&fontname=cuddly&width=$COLUMNS"
curl -s -X GET "http://localhost:5000/api/banner?message=whatever&fontname=cuddly&width=0"
curl -s -X GET "http://localhost:5000/api/banner?message=CIRCLE%20CI&fontname=knight4&width=$COLUMNS"

# get banners 
echo $(curl -s -X GET --header 'Accept: text/plain' "http://localhost:5000/api/banner?message=whatever&fontname=cuddly&width=165" | sed 's/^\"\(.*\)\"$/\1/' )        
echo $(curl -s -X GET --header 'Accept: text/plain' "http://localhost:5000/api/banner?message=whatever&fontname=cuddly&width=$COLUMNS" | sed 's/^\"\(.*\)\"$/\1/' ) 
echo $(curl -s -X GET --header 'Accept: text/plain' "http://localhost:5000/api/banner?message=whatever&fontname=cuddly&width=0" | sed 's/^\"\(.*\)\"$/\1/' ) 
echo $(curl -s -X GET --header 'Accept: text/plain' "http://localhost:5000/api/banner?message=CIRCLE%20CI&fontname=knight4&width=$COLUMNS" | sed 's/^\"\(.*\)\"$/\1/' )
```

## Load Test
```sh
# install artillery
npm install -g artillery

# run artillery trests
artillery run ./tests/artillery/generate.yml
```