"""
This python code implements the back-end for the smart photo storage hosted on a home server
Written by: Sai Keshav Sasanapuri @Skeshav-sasanapuri
"""

# Importing libraries
import os
from flask import Flask, request, jsonify, flash
from werkzeug.utils import secure_filename
from PIL import Image
from PIL.ExifTags import TAGS
from datetime import datetime
from pymongo import MongoClient
from flask_cors import CORS  # Import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

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
    print(filename)
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

    return jsonify({"message": "Files uploaded successfully!"}), 200


# Endpoint for retrieving photos
@app.route('/photos', methods=['GET'])
def get_photos():
    print("came here, back")
    query = {}

    # Get filter parameters from query string
    date_taken = request.args.get('date_taken')
    tag = request.args.get('tag')

    # Filter by date_taken if provided
    if date_taken:
        try:
            date_obj = datetime.strptime(date_taken, '%Y-%m-%d').date()  # Adjust format if needed
            query['date_taken'] = date_obj.strftime('%Y-%m-%d')  # Match the format in the database
        except ValueError:
            flash("Invalid date format. Please use YYYY-MM-DD.", "error")
            return jsonify({"error": "Invalid date format."}), 400

    # Handle multiple tags
    if tag:
        tags_list = [t.strip() for t in tag.split(',')]
        query['tag'] = {'$in': tags_list}  # Match any of the specified tags

    # Retrieve photo documents from MongoDB based on the query
    photo_docs = list(photos_collection.find(query, {'_id': 0}))  # Exclude MongoDB _id field from results

    # Prepare the response list with full data
    photos = []
    for doc in photo_docs:
        photo_path = doc.get('path')  # Use the full path from MongoDB directly
        if os.path.exists(photo_path):  # Check if the photo exists on the server
            photo_data = {
                'path': photo_path,  # Keep the full path for the response
                'filename': os.path.basename(photo_path),  # Extract filename from the path
                'date_taken': doc.get('date_taken'),  # Add other relevant fields from MongoDB
            }
            photos.append(photo_data)

    return jsonify(photos), 200



# Test route to ensure the server is working
@app.route('/')
def home():
    return jsonify({"message": "Server is up and running!"})


if __name__ == '__main__':
    # Create the uploads directory if it doesn't exist
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)
