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

app = Flask(__name__)

# Directory to store uploaded images
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allowed extensions for uploaded files
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


# Function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Function to extract the date from the image's EXIF data
def extract_date_taken(image):
    try:
        exif_data = image._getexif()
        if exif_data is not None:
            # Directly access the DateTimeOriginal tag using its ID (306)
            date_time_original = exif_data.get(306)  # 306 is the tag for DateTimeOriginal
            if date_time_original:
                # Parse and return the date
                return datetime.strptime(date_time_original, '%Y:%m:%d %H:%M:%S').date()
    except Exception as e:
        print(f"Error extracting date: {e}")
    return None


# Endpoint for uploading images
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request."}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No file selected."}), 400

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

        return jsonify(
            {"message": "File uploaded successfully!", "filename": filename, "date_taken": str(date_taken)}), 201

    return jsonify({"error": "File type not allowed."}), 400


# Test route to ensure the server is working
@app.route('/')
def home():
    return jsonify({"message": "Server is up and running!"})

if __name__ == '__main__':
    # Create the uploads directory if it doesn't exist
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)
