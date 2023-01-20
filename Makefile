create-environment : 
	pyenv virtualenv venv_graph_project

activate-environment : 
	pyenv activate venv_graph_project

install-requirements : 
	pip install -r ./requirements_dev.txt
	pip install -r ./src/requirements.txt

build-images : 
	docker build -f "Dockerfile.terraform_python" -t "graph-project-terraform-python" "."
	docker build -f "Dockerfile.postgres" -t "graph-project-postgres" "."
	docker build -f "Dockerfile.local_stack" -t "graph-project-local-stack" "."

docker-compose : 
	make build-images
	docker compose up

ssh-localstack : 
	docker exec -it localstack /bin/bash

split-raw-data : 
	cat src/resources/original_data/bank_fraud_raw_data.csv | parallel --header : --pipe -N10 'cat > src/resources/split_data/fraud_data_partition_{#}.csv'

send-new-data-to-bucket : 
	docker exec -it localstack \
		awslocal s3 cp \
		./split_data/fraud_data_partition_$(index_file).csv \
		s3://project-bucket/new_data/fraud_data_partition_$(index_file).csv

list-objects-in-bucket : 
	docker exec -it localstack awslocal s3 ls s3://project-bucket --recursive --human-readable --summarize

list-lambda-functions : 
	docker exec -it localstack awslocal lambda list-functions

test-lambda : 
	docker exec -it localstack awslocal lambda invoke \
		--function-name $(function_name) \
		./output_test.log