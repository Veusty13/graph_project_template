#!/bin/sh

rm -r ./postgres/
psql -U postgres -c "drop database if exists graph_project"
psql -U postgres -c "CREATE DATABASE graph_project"
psql -U postgres -c "grant all privileges on database graph_project to postgres"
psql -U postgres -d graph_project -c "CREATE TABLE transactions (
  id INT PRIMARY KEY,
  step NUMERIC,
  type VARCHAR(255),
  amount NUMERIC(11,2), 
  nameOrig VARCHAR(255),
  oldbalanceOrg NUMERIC(11,2),
  newbalanceOrig NUMERIC(11,2), 
  nameDest VARCHAR(255),
  oldbalanceDest NUMERIC(11,2),
  newbalanceDest NUMERIC(11,2),
  isFraud BOOLEAN,
  isFlaggedfraud BOOLEAN
);" 
echo "successfully created project table with the following schema"
psql -U postgres -d graph_project -c "SELECT 
   table_name, 
   column_name, 
   data_type 
FROM 
   information_schema.columns
WHERE 
   table_name = 'transactions';"
