# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any dependencies specified in requirements.txt
# If you don't have a requirements.txt, you can install dependencies directly
# RUN pip install --no-cache-dir -r requirements.txt

# Command to run the application
CMD ["python", "game.py"]