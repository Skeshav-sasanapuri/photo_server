#!/bin/bash

# Start MongoDB
echo "Starting MongoDB..."
mongod --dbpath "C:\\data\\db" --bind_ip 127.0.0.1 &  # Adjust the dbpath as needed

# Give MongoDB a moment to start
sleep 10

# Start Flask application
echo "Starting Flask application..."
python app.py  # Adjust the path to your Flask app
