# Use an official Python runtime as a parent image
FROM python:2.7-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
FROM ubuntu:16.04
RUN apt-get update
RUN apt-get install -y python-pip ngrok-client
RUN pip install -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV NAME Alexa

# Run app.py when the container launches
CMD ["python", "app.py"]
