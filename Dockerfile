# Use an official Python runtime as a parent image
FROM python:3.6-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
# RUN pip install --trusted-host pypi.python.org -r requirements.txt
RUN pip install pipenv
RUN pipenv install --system

# Make collect-tweets executable
CMD ["chmod", "u+x", "collect-tweets"]

