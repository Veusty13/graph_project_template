#!/bin/sh


apt-get update -y
apt-get install libpq-dev -y
apt-get install gcc -y
pip install --upgrade pip
pip install -r ./src/requirements.txt --target ./lambda_dependencies/
cp -a ./src/. ./lambda_package/
cp -a ./lambda_dependencies/. ./lambda_package/function/
ls -a lambda_package
ls -a lambda_package/function