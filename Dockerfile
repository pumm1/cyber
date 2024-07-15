# Use the official Python image from the Docker Hub
FROM python:3.10

# Set the working directory in the container
WORKDIR /

# Copy the requirements file into the container
COPY requirements.txt ./

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt \
    && apt-get update \
    && apt-get install -y nano postgresql-client net-tools iproute2 iputils-ping


# Copy the rest of the application code into the container
COPY src /src
COPY db /db
COPY src/secrets_docker.json /src/secrets.json

RUN pip install flask

COPY wait-for-postgres.sh /wait-for-postgres.sh
RUN chmod +x /wait-for-postgres.sh

# Specify the command to run on container start
CMD ["./wait-for-postgres.sh", "cyber_db", "flask", "--app", "src/net/app", "run"]
