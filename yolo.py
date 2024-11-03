import time
from pymongo import MongoClient
from ultralytics import YOLO

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['photo_storage']  # Database name
photos_collection = db['photos']  # Collection for photos
unprocessed_ids_collection = db['unprocessed_ids']  # Collection for unprocessed IDs

# Define the confidence threshold
CONFIDENCE_THRESHOLD = 0.3  # Adjust this value based on your needs

def process_image(document_id):
    print("Processing image with ID:", document_id)

    # Look up the photo in the photos collection
    photo_metadata = photos_collection.find_one({'_id': document_id})

    if photo_metadata:
        file_path = photo_metadata['path']

        # Load YOLOv8 model
        model = YOLO('yolov8m.pt')  # Adjust the model as needed

        # Perform inference
        results = model(file_path)

        # Filter detected classes based on confidence threshold
        tags = set()

        # Loop through each result (if results are in multiple frames or detections)
        for result in results:
            # Access the detection boxes and their attributes
            boxes = result.boxes  # Get the bounding boxes
            if boxes is not None:
                for box in boxes:
                    # Get class label and confidence score
                    class_id = int(box.cls)  # Class index
                    conf = box.conf  # Confidence score

                    # Get the class name from the model's names list
                    class_name = result.names[class_id]

                    # Check against the confidence threshold
                    if conf >= CONFIDENCE_THRESHOLD:
                        tags.add(class_name)

        # Update the photos collection with detected tags
        photos_collection.update_one(
            {'_id': document_id},
            {'$set': {'tag': list(tags)}}  # Update with detected tags
        )

        # Remove the document ID from the unprocessed_ids collection
        unprocessed_ids_collection.delete_one({'_id': document_id})

        print(f"Processed {file_path} with tags: {tags}")
    else:
        print(f"No photo found with ID: {document_id}")

def main():
    print("YOLO processor is running...")
    while True:
        # Check for unprocessed IDs
        unprocessed_id = unprocessed_ids_collection.find_one()

        if unprocessed_id:
            print("Unprocessed image found. Begin Processing")
            document_id = unprocessed_id['_id']
            process_image(document_id)
        else:
            print("No unprocessed images found. Waiting...")

        time.sleep(5)  # Sleep for a while before checking again

if __name__ == '__main__':
    main()
