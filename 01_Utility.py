# Databricks notebook source
password = "" #Use your OAuth Token from respective OLTP-Database instance
driver = "org.postgresql.Driver"
user = "example@databricks.com" #User having access to database instance
database_host = "instance-3d8076e6-3884-4c74-b7ef-3fd539504f6c.database.azuredatabricks.net" #Your databricks host instance name
database_port = "5432"
database_name = "databricks_postgres" #Name of your database

# COMMAND ----------

# Setting the above parameters as env variables for reusability
import os
os.environ["PASSWORD"] = password
os.environ["user"] = user
os.environ["database_host"] = database_host
os.environ["database_port"] = database_port
os.environ["database_name"] = database_name
