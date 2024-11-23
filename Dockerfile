# Use the official Python image from Docker Hub
FROM python:3.8.2-alpine

# Set environment variables to prevent Python from writing pyc files to disc
# and to run in non-interactive mode
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt /app/

# Install the Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the application files into the container
COPY . /app/

# Specify the command to run the Python application
CMD ["python", "main.py"]
