#!/bin/bash

# Delay the script until mariadb is up
until nc -z -v -w30 172.20.0.10 3306
do
  echo "Waiting for database connection..."
  # wait for 5 seconds before check again
  sleep 5
done

# Create database using mysqldump
mysql -u root -h 172.20.0.10 -p123thisisatest! epitaxy_db < db_structure.sql


# Start server
echo "Starting server"
python manage.py runserver 0.0.0.0:8000