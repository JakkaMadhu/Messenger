# Use a lightweight official Python runtime as base
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Install Tkinter system dependency (APT resolves other X11 requirements automatically)
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-tk \
    && rm -rf /var/lib/apt/lists/*

# Copy and install client requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the client code
COPY . .

# Default display server address pointing to the host's virtual X-server
ENV DISPLAY=host.docker.internal:0.0

# Start the Tkinter client application
CMD ["python", "messenger.py"]
