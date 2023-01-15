#!/bin/sh

rm -r ./postgres/
psql -U postgres -c "drop database if exists graph_project"
psql -U postgres -c "CREATE DATABASE graph_project"
psql -U postgres -c "grant all privileges on database graph_project to postgres"
psql -U postgres -d graph_project -c "CREATE TABLE supplies (
  id INT PRIMARY KEY,
  name VARCHAR,
  description VARCHAR,
  manufacturer VARCHAR,
  color VARCHAR,
  inventory int CHECK (inventory > 0)
);" 
echo "successfully created project table with the following schema"
psql -U postgres -d graph_project -c "SELECT 
   table_name, 
   column_name, 
   data_type 
FROM 
   information_schema.columns
WHERE 
   table_name = 'supplies';"