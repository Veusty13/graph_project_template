# graph_project_template
A simple project that shows how tabular data can be converted into graph data.
This repo uses an `AWS` infrastructure and additional services such as `postgres` and `gremlin-server`.
A visualization tool is available to have a look at the graph but also to interact with it using gremlin queries.

# quick start

- `make docker-compose` to build all necessary images and setup the containers, make sure all containers are ready before moving to the next step
- `make split-raw-data` to split original data into several smaller datasets
- `make send-single-partition-to-bucket index_partition=1` to send the first partition to the folder `new_data/` in the s3 bucket, you can repeat this command to transfer all the partitions, for example `index_partition=2` if you want to send the second partition
- `make test-lambda function_name=trigger-processing-function` if you want to trigger lambdas in charge of updating the graph. You could also wait for the lambda functions to trigger themselves as a cron is running and triggers the functions every 3 minutes

Once the graph is uploaded with tabular data, open your web browser and reach the url : `localhost:3000`.
You can interact with the graph using gremlin queries.

# architecture of the project

- a new file containing tabular data is uploaded to an s3 bucket in a specific folder
- a cron will trigger a lambda that will move this file to another folder so that an s3 event is generated
- event message is sent to a lambda using SQS to feed a postgres table
- once data is added another lambda will refresh the graph containing the information

# set up your python environment to develop
I suggest the use of `pyenv` to manage your python versions and your environment without using your system version of `python`.
It is a good practice to avoid using the system version of python as some projects require the use of several versions of python. 
For more information about the installation of `pyenv`, the installation of a version of `python`, the creation of an environment using this tool please check this link : https://akrabat.com/creating-virtual-environments-with-pyenv/
If you are using `Visual Studio Code` editor, you can download the plugin `Python Environment Manager` as it gives you a nice overview of the different versions of `python` and the different environments created in your machine.


# dependencies of the project
- `python` : the programming language that is used on the server side
- `terraform` : is an open-source infrastructure as code software tool that enables you to safely and predictably create, change, and improve the infrastructure of this project
- `LocalStack` : to run AWS applications or Lambdas entirely on a local machine without connecting to a remote cloud provider
- `Docker` : to packages code and its dependencies so the application runs quickly and reliably across computing environments
- `aws-cli` : a command line interface to interact with `AWS` objects

# data source
For this project we will use synthetic bank data available here : https://www.kaggle.com/datasets/ealaxi/paysim1
However, we use a modified version of this dataset.