# graph_project_template
Project that aims at being a template for any project where a graph structure is involved.
Typically : 
- a new file containing tabular data is uploaded to an s3 bucket in a specific folder
- a cron will trigger a lambda that will move this file to another folder so that an s3 event is generated
- event message is sent to a lambda using SQS to feed a postgres table
- once data is added another lambda will refresh the graph containing the information thanks to a dedicated API