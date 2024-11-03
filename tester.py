import cv2

# Path to the image you want to open
image_path = "C://Users//kesha//PycharmProjects//photo_server//uploads//2024-09-26//test image.jpg"

# Read the image using OpenCV
image = cv2.imread(image_path)

# Check if the image was loaded successfully
if image is None:
    print("Error: Could not open or find the image.")
else:
    # Display the image in a window
    cv2.imshow('Image', image)

    # Wait for a key press and close the window
    cv2.waitKey(0)
    cv2.destroyAllWindows()