#!/bin/sh

rm src/*.zip

cd infra/

terraform init

terraform plan

terraform apply -auto-approve

cd ..

rm src/*.zip