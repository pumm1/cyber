# Use the official Python image from the Docker Hub
FROM python:3.10

# Set the working directory in the container
WORKDIR /

# Copy the requirements file into the container
COPY requirements.txt ./

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY src /src
COPY db /db

RUN pip install flask

# Specify the command to run on container start
CMD ["flask", "--app", "src/net/app", "run"]
