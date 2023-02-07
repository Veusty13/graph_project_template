# graph_project_template
Project that aims at being a template for any project where a graph structure is involved.
Typically : 
- a new file containing tabular data is uploaded to an s3 bucket in a specific folder
- a cron will trigger a lambda that will move this file to another folder so that an s3 event is generated
- event message is sent to a lambda using SQS to feed a postgres table
- once data is added another lambda will refresh the graph containing the information thanks to a dedicated API

# architecture of the project

# set up your python environment to run this project
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