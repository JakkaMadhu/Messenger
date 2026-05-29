# Use a lightweight official Python runtime as base
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Copy and install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the server application code
COPY . .

# Expose the TCP port configured in config.py
EXPOSE 45999

# Start the TCP listening server
CMD ["python", "server.py"]
