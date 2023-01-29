#!/bin/sh

python3.8 --version
python3.8 -m pip install --upgrade pip
python3.8 -m pip install -r ./src/requirements.txt --target ./lambda_dependencies/
mkdir lambda_package
cp -a ./src/. ./lambda_package/
cp -a ./lambda_package/function/. ./lambda_package/
rm -r ./lambda_package/function/
cp -a ./lambda_dependencies/. ./lambda_package/

cd infra/
terraform init
terraform plan
terraform apply -auto-approve