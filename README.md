# pic-back


## dev

Run dev server
```sh
./scripts/run_dev.sh
```

To use scripts
```sh
export PYTHONPATH="${PYTHONPATH}:~/projects/pic-back"
```

To run app first time, token.json has to be generated with `gcredentials.py` but first download credentials from developer console. Token should be valid all the time (production app).

coords (6 decimal)
```
43.213671
```

Dockerize
```
docker build . --tag pic-back-image
docker run pic-back-image
docker-compose up
```
