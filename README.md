# README


## Docker image
```sh
# build image
docker build -t banner_service .


docker run -e COLUMNS=${COLUMNS} -e TERM=${TERM} banner_service
```

