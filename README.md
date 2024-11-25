
# My Cloud  
A self-hosted, open-source photo storage application inspired by Google Photos. This project combines AI-powered image tagging, seamless search and filtering, and an intuitive, accessible interface to provide a robust photo management solution.

## Features  
- **AI-Powered Tagging**: Automatically tags uploaded images using YOLOv8 object detection.  
- **Effortless Search & Filtering**: Search photos by tags or filter them by date with ease.  
- **Seamless Uploads**: Upload multiple images directly and quiclkly through the web interface. Image processing and feature extraction happens asynchronously in the back end.  
- **Self-Hosted Storage**: Complete ownership of your photos with local storage.  
- **Responsive Frontend**: Designed with Bootstrap and jQuery for a clean, accessible, and user-friendly experience.  
- **RESTful API**: Backend API powered by Flask for handling uploads, searches, and metadata management.  
- **Database Management**: MongoDB used for efficient storage and querying of image metadata.  

## Demo  
- **Search & Filter**: Use tags and date filters to find images in a grid view.  
- **Upload Photos**: Upload single or multiple photos to your local server, with AI processing tags in the background.  
- **Tagging Automation**: Watch uploaded images automatically tagged with detected objects for better organization.  

## Installation  
### Prerequisites  
- Python 3.8+  
- MongoDB  
- Flask 

### Steps  
1. Clone the repository:  
   ```bash
   git clone https://github.com/Skeshav-sasanapuri/photo_server.git
   cd photo_server
   ```
2. Set up a virtual environment and install dependencies:  
   ```bash 
   pip install -r requirements.txt  
   ```
3. Start MongoDB on your local system or connect to your MongoDB server.  
4. Run the Flask backend:  
   ```bash
   python app.py  
   ```
5. Open the app in your browser.  

## Technologies Used  
- **Backend**: Flask  
- **Frontend**: Bootstrap, jQuery  
- **AI Model**: YOLOv8 for object detection  
- **Database**: MongoDB  
- **Languages**: Python, JavaScript  
- **Hosting**: Self-hosted on local server  

## Project Architecture  
1. **Frontend**:  
   - Uses Bootstrap for styling and responsive design.  
   - jQuery handles AJAX requests to the backend API.  

2. **Backend**:  
   - Flask provides REST endpoints for handling image uploads, metadata retrieval, and search queries.  
   - RabbitMQ (optional) can be integrated for asynchronous processing.  

3. **Database**:  
   - MongoDB stores image metadata such as file paths, tags, and dates.  

4. **AI Processing**:  
   - YOLOv8 detects objects in uploaded images, adding relevant tags stored in the database.    

## Future Improvements  
- Add support for cloud-based storage solutions.  
- Support for videos.  
- Advanced filtering options such as location-based search.  

## License  
This project is open-source under the MIT License.  

## Acknowledgements  
- Inspired by Google Photos' simplicity and functionality.  
- YOLOv8 for its state-of-the-art object detection capabilities.  

## Contributing  
Contributions are welcome! Please fork the repository and submit a pull request with your changes.

---

Start managing your photos your way with **My Cloud**! 🌟
