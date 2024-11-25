
# My Cloud  
A self-hosted, open-source photo storage application inspired by Google Photos. This project combines AI-powered image tagging, seamless search and filtering, and an intuitive, accessible interface to provide a robust photo management solution.

## Features  
- **AI-Powered Tagging**: Automatically tags uploaded images using YOLOv8 object detection.  
- **Effortless Search & Filtering**: Search photos by tags or filter them by date with ease.  
- **Seamless Uploads**: Upload multiple images directly through the web interface.  
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
- Node.js and npm (optional for frontend testing)

### Steps  
1. Clone the repository:  
   ```bash
   git clone https://github.com/your-username/my-cloud.git  
   cd my-cloud  
   ```
2. Set up a virtual environment and install dependencies:  
   ```bash
   python3 -m venv venv  
   source venv/bin/activate  # On Windows: venv\Scripts\activate  
   pip install -r requirements.txt  
   ```
3. Start MongoDB on your local system or connect to your MongoDB server.  
4. Run the Flask backend:  
   ```bash
   python app.py  
   ```
5. Open the app in your browser at [http://127.0.0.1:5000](http://127.0.0.1:5000).  

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

## Accessibility  
This project was designed with accessibility in mind, featuring:  
- High-contrast dark mode.  
- Large, readable fonts.  
- Accessible forms and buttons.  

## Screenshots  
### Home Page  
![Home Page](screenshots/homepage.png)  

### Search and Filter  
![Search and Filter](screenshots/search.png)  

### Upload Photos  
![Upload Photos](screenshots/upload.png)  

## Future Improvements  
- Add support for cloud-based storage solutions.  
- Real-time object detection for faster processing.  
- Advanced filtering options such as object categories and location-based search.  

## License  
This project is open-source under the MIT License.  

## Acknowledgements  
- Inspired by Google Photos' simplicity and functionality.  
- YOLOv8 for its state-of-the-art object detection capabilities.  

## Contributing  
Contributions are welcome! Please fork the repository and submit a pull request with your changes.

---

Start managing your photos your way with **My Cloud**! 🌟
