create-environment : 
	pyenv virtualenv venv_graph_project

activate-environment : 
	pyenv activate venv_graph_project

install-requirements : 
	pip install -r requirements.txt

docker-compose : 
	docker compose up

split-raw-data : 
	cat src/resources/original_data/bank_fraud_raw_data.csv | parallel --header : --pipe -N30000 'cat > src/resources/split_data/fraud_data_partition_{#}.csv'