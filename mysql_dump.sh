#!/bin/bash

# Define the MySQL connection details
local_host="localhost"
local_user="root"
local_password="mysql8"
local_database="djangoblog"
local_port="3306"

# Dump the local MySQL database
mysqldump -h $local_host -P $local_port -u $local_user -p$local_password $local_database > /data/blogdata_dump.sql

echo "MySQL database dump complete!"
