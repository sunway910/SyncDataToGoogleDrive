#!/bin/bash

# Define the MySQL connection details
local_host="localhost"
local_port="3306"
local_user="root"
local_password="xxxxxxxxxxxxxxxx"
local_database="djangoblog"


# Dump the local MySQL database
mysqldump -h $local_host -P $local_port -u $local_user -p$local_password $local_database > /data/blog_image_data/blogdata_dump.sql

echo "MySQL database dump complete!"
