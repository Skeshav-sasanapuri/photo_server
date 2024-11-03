"""
This python code implements the back-end for the smart photo storage hosted on a home server
Written by: Sai Keshav Sasanapuri @Skeshav-sasanapuri
"""

# Importing libraries
import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from PIL import Image
from PIL.ExifTags import TAGS
from datetime import datetime
from pymongo import MongoClient
from yolo import process_image

app = Flask(__name__)

# Directory to store uploaded images
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allowed extensions for uploaded files
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# MongoDB connection setup
client = MongoClient('mongodb://localhost:27017/')  # Change connection based on type of implementation
db = client['photo_storage']  # Database name
photos_collection = db['photos']  # Collection name
unprocessed_ids_collection = db['unprocessed_ids']  # Collection for unprocessed IDs


# Function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Function to extract the date from the image's EXIF data
def extract_date_taken(image):
    try:
        exif_data = image._getexif()
        if exif_data is not None:
            date_time_original = exif_data.get(306)  # 306 is the tag for DateTimeOriginal
            if date_time_original:
                return datetime.strptime(date_time_original, '%Y:%m:%d %H:%M:%S').date()
    except Exception as e:
        print(f"Error extracting date: {e}")
    return None


# Endpoint for uploading images
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'files[]' not in request.files:
        return jsonify({"error": "No file part in the request."}), 400

    files = request.files.getlist('files[]')

    if not files:
        return jsonify({"error": "No file selected."}), 400
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            # Open the file in memory and extract the date taken
            image = Image.open(file)
            date_taken = extract_date_taken(image)

            # Use current date if EXIF data has no date information
            if date_taken is None:
                date_taken = datetime.today().date()

            # Define the final directory and save path
            date_folder = os.path.join(app.config['UPLOAD_FOLDER'], str(date_taken))
            os.makedirs(date_folder, exist_ok=True)
            file_path = os.path.join(date_folder, filename)

            # Save the file directly to the target folder
            file.seek(0)  # Reset file pointer after reading for EXIF
            file.save(file_path)

            # Prepare metadata to save to MongoDB
            metadata = {
                'filename': filename,
                'path': file_path,
                'upload_date': datetime.now(),
                'date_taken': date_taken.strftime('%Y-%m-%d'),
                'tag': []  # Initialize tags to store YOLO detections
            }

            # Insert metadata into MongoDB
            insert_result = photos_collection.insert_one(metadata)
            document_id = insert_result.inserted_id

            # Store the document ID in the unprocessed_ids collection for YOLO to process
            unprocessed_ids_collection.insert_one({'_id': document_id})

    return jsonify(
        {"message": "Files uploaded successfully!"}), 201




# Endpoint for retrieving photos
@app.route('/photos', methods=['GET'])
def get_photos():
    query = {}

    # Get filter parameters from query string
    date_taken = request.args.get('date_taken')
    tag = request.args.get('tag')

    # Filter by date_taken if provided
    if date_taken:
        query['date_taken'] = date_taken

    # For now, let's just use the filename as a simple example of a tag
    if tag:
        query['filename'] = {'$regex': tag, '$options': 'i'}  # Case-insensitive match

    # Retrieve photos from MongoDB based on the query
    photos = list(photos_collection.find(query, {'_id': 0}))  # Exclude MongoDB _id field from results

    return jsonify(photos), 200


# Test route to ensure the server is working
@app.route('/')
def home():
    return jsonify({"message": "Server is up and running!"})


if __name__ == '__main__':
    # Create the uploads directory if it doesn't exist
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)
