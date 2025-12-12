#!/usr/bin/env bash

echo "Deploying..."

cd pic-back
date
date > last_update_start.txt
git pull
docker compose build
docker compose down
docker compose up --detach

echo "Deploy finished!"
date
date > last_update_end.txt
