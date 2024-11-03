# None ARM Target 
# FROM python:3.13-slim 

# ARM Target (For example Pi5)
FROM arm64v8/python:3.13-slim 

WORKDIR /app

# Install dependencies
RUN apt-get update && \
    apt-get install -y ffmpeg libffi-dev libssl-dev && \
    rm -rf /var/lib/apt/lists/*

RUN pip install opencv-python opencv-contrib-python
RUN pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib 

# Create necessary directories
RUN mkdir -p /app/timelapse/

# Copy project files
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .


# Run the script
ENTRYPOINT  ["python", "-u", "capture.py"]