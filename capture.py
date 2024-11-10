import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'env')))
import config

import cv2
import time
from datetime import datetime
import io
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from google.oauth2 import service_account
import threading
# Replace with your RTSP URL

SERVICE_ACCOUNT_FILE = 'env/key.json'  # Path to your key file inside the container
SCOPES = ['https://www.googleapis.com/auth/drive.file','https://www.googleapis.com/auth/drive'] 
creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Build the Google Drive API service
service = build('drive', 'v3', credentials=creds)

# Set the interval for taking screenshots (in seconds)
dir = "timelapse"

def capture_screenshot():
    """Captures a screenshot from the RTSP stream and saves it with a timestamp."""
    try:
        # Create a VideoCapture object
        cap = cv2.VideoCapture(config.RTSP_URL)

        # Check if the camera opened successfully
        if not cap.isOpened():
            print("Error opening video stream or file")
            return

        # Read a frame from the stream
        ret, frame = cap.read()

        if ret:
            # Generate a timestamp for the filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            filename = f"screenshot_{timestamp}.jpg"

            # Save the frame as an image
            cv2.imwrite(f"{dir}/{filename}", frame)
            print(f"Screenshot saved as {filename}")

            # Upload the captured image to Google Drive
            if upload_to_drive(filename):  # Check if upload was successful
                os.remove(f"{dir}/{filename}")  # Delete the local file
                print(f"Local file {filename} deleted.")
        else:
            print("Error reading frame")

        # Release the VideoCapture object
        cap.release()

    except Exception as e:
        print(f"An error occurred: {e}")
def upload_to_drive(filename, retries=3, backoff_factor=2):
    """Uploads with retry and exponential backoff."""
    try:
        file_metadata = {'name': filename, 'parents': [config.FOLDER_ID]}  # Replace with your folder ID
        media = MediaIoBaseUpload(io.BytesIO(open(f"{dir}/{filename}", 'rb').read()),
                                    mimetype='image/jpeg')
        file = service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()
        print(f'File ID: {file.get("id")} uploaded to Google Drive')
        return True  # Upload successful

    except BrokenPipeError as e:
        print(f"Broken pipe error: {e}")
        if retries > 0:
            wait_time = backoff_factor ** (3 - retries)  # Exponential backoff
            print(f"Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
            return upload_to_drive(filename, retries - 1, backoff_factor)
        else:
            print("Max retries reached. Upload failed.")
            return False

    except Exception as e:
        print(f"An error occurred while uploading: {e}")
        return False  # Upload failed


if __name__ == '__main__':
    print("START")
    
    # Use a while loop and time.sleep() to control the interval
    while True:
        start_time = time.time()  # Get the start time

        capture_screenshot()

        end_time = time.time()  # Get the end time
        execution_time = end_time - start_time

        # Adjust the sleep time to maintain the interval
        if execution_time < config.SCREENSHOT_INTERVAL:
            time.sleep(config.SCREENSHOT_INTERVAL - execution_time) 


