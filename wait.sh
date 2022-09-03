#!/bin/bash

while ! nc -z db 3306 ; do
    echo "Waiting for the MySQL database server to start on port 3306 properly"
    sleep 5
done