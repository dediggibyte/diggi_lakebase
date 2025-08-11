# Databricks notebook source
# DBTITLE 1,install
# MAGIC %sh 
# MAGIC sudo apt-get update && sudo apt-get install -y postgresql-client

# COMMAND ----------

# MAGIC %sh
# MAGIC
# MAGIC sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
# MAGIC
# MAGIC
# MAGIC wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
# MAGIC
# MAGIC # Update apt
# MAGIC sudo apt update

# COMMAND ----------

# MAGIC %sh
# MAGIC sudo apt install -y postgresql-14 postgresql-contrib-14

# COMMAND ----------

# MAGIC %sh 
# MAGIC ls /usr/lib/postgresql/14/bin/pgbench

# COMMAND ----------

# MAGIC %sh
# MAGIC echo 'export PATH="/usr/lib/postgresql/14/bin:$PATH"' >> ~/.bashrc
# MAGIC source ~/.bashrc

# COMMAND ----------

# MAGIC %sh
# MAGIC pgbench --version

# COMMAND ----------

# MAGIC %run ./01_Utility

# COMMAND ----------

# MAGIC %sh
# MAGIC
# MAGIC #echo ""$PASSWORD
# MAGIC echo "CONNECTION DETAILS : database_host="$database_host
# MAGIC echo "CONNECTION DETAILS : database_name="$database_name
# MAGIC echo "CONNECTION DETAILS : database_port="$database_port
# MAGIC echo "CONNECTION DETAILS : user= "$user
# MAGIC export PGPASSWORD=$PASSWORD
# MAGIC
# MAGIC pgbench -n -h $database_host -p $database_port -U $user \
# MAGIC         -f custom_test.sql \
# MAGIC         -T 180 \
# MAGIC         -c 180 \
# MAGIC         -j 6 \
# MAGIC          $database_name
