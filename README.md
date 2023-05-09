# s3-rotation-files
I need one container with connect on s3 and dele all archives with more X days


# Prepare Requirements

`pip freeze > app/requirements.txt`

# Local test

```bash
docker build . -t  s3-rotation-files:0.0.1-rc
docker run --rm --env FILE_AGE="15" -v $(pwd)/app/config/:/app/config/ s3-rotation-files:0.0.1-rc
```

# Requeriments for docker

envoriment with FILE_AGE and volume with bucket.yaml on app/config