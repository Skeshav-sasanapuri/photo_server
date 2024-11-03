#!/bin/bash

# Start MongoDB
echo "Starting MongoDB..."
mongod --dbpath "C:\\data\\db" --bind_ip 127.0.0.1 --logpath "mongodb.log" &
sleep 5  # Give MongoDB time to start

# Start Flask application in production mode
echo "Starting Flask application..."
python app.py &
sleep 5  # Give Flask time to start

echo "Starting YOLO processor for Images"
python yolo.py &

echo "All services started."

# Keep the script running to allow Ctrl+C to kill all background processes
wait
