#!/bin/sh

rm ./lambda_package/

pip install --upgrade pip
pip install -r ./src/requirements.txt --target ./lambda_dependencies/
mkdir lambda_package
cp -a ./src/. ./lambda_package/
cp -a ./lambda_dependencies/. ./lambda_package/function/

cd infra/
terraform init
terraform plan
terraform apply -auto-approve

rm ./lambda_package/