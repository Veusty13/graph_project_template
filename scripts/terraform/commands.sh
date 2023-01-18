#!/bin/sh

rm src/function.zip

cd infra/

terraform init

terraform plan

terraform apply -auto-approve

cd ..

rm src/function.zip