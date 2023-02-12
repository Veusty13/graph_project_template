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
	docker build -f "Dockerfile.gremlin" -t "graph-project-gremlin" "."

docker-compose : 
	make build-images
	docker image prune -f 
	docker compose up

ssh-localstack : 
	docker exec -it graph-project-local-stack /bin/bash

ssh-postgres : 
	docker exec -it graph-project-postgres /bin/bash

ssh-gremlin-console : 
	docker exec -it graph-project-gremlin-console /bin/bash bin/gremlin.sh

split-raw-data : 
	cat resources/original_data/bank_fraud_raw_data.csv | parallel --header : --pipe -N50000 'cat > resources/split_data/fraud_data_partition_{#}.csv'

send-single-partition-to-bucket : 
	docker exec -it graph-project-local-stack \
		awslocal s3 cp \
		./split_data/fraud_data_partition_$(index_partition).csv \
		s3://project-bucket/new_data/fraud_data_partition_$(index_partition).csv

send-all-partitions-to-bucket: 
	docker exec -it graph-project-local-stack \
		awslocal s3 cp \
		./split_data/ \
		s3://project-bucket/new_data/ --recursive

list-objects-in-bucket : 
	docker exec -it graph-project-local-stack awslocal s3 ls s3://project-bucket --recursive --human-readable --summarize

list-lambda-functions : 
	docker exec -it graph-project-local-stack awslocal lambda list-functions

list-sqs-queues : 
	docker exec -it graph-project-local-stack awslocal sqs list-queues

test-lambda : 
	docker exec -it graph-project-local-stack awslocal lambda invoke \
		--function-name $(function_name) \
		./output_test.log

query-read-table : 
	docker exec -it graph-project-local-stack psql -U postgres -d graph_project -c "select * from transactions;"