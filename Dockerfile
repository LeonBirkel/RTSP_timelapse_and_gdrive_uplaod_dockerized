
# None ARM Target => ARG TARGET_ARCH=amd64
# ARM Target (For example Pi5) => ARG TARGET_ARCH=arm64v8
ARG TARGET_ARCH=amd64 

FROM ${TARGET_ARCH}/python:3.13-slim 

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libgl1-mesa-glx \
        libglib2.0-0 \
    && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
    
# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Create necessary directories
RUN mkdir -p /app/timelapse/

COPY . .


# Run the script
ENTRYPOINT  ["python", "-u", "capture.py"]