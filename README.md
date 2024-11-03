# RTSP Timelapse and Google Drive Upload (Dockerized)

This project captures timelapse images from an RTSP camera stream and automatically uploads them to Google Drive. It's designed to run efficiently in a Docker container, making it easy to deploy on various platforms, including a Raspberry Pi.

## Features

- Captures images from an RTSP camera stream at specified intervals.
- Uploads captured images to a Google Drive folder.
- Deletes local image copies after successful uploads (optional).
- Dockerized for easy deployment and portability.
- Configurable settings for camera URL, Google Drive credentials, and time interval.

## Requirements

- **Docker:**  Installed on your host machine (e.g., Raspberry Pi, server, or local computer).
- **RTSP Camera:** An IP camera that provides an RTSP stream.
- **Google Drive Account:** A Google account with a folder to store the timelapse images.
- **Service Account:** A Google Cloud service account with permissions to upload files to your Google Drive folder.

## Setup

1. **Clone the Repository:**

   ```bash
   git clone [https://github.com/LeonBirkel/RTSP_timelapse_and_gdrive_uplaod_dockerized](https://github.com/LeonBirkel/RTSP_timelapse_and_gdrive_uplaod_dockerized)
   cd RTSP_timelapse_and_gdrive_uplaod_dockerized
