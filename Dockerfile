FROM python:latest
WORKDIR /
RUN pip install --upgrade pip
ADD src/requirements.txt src/requirements.txt
ADD src/secrets.json src/secrets.json
RUN pip install -r /src/requirements.txt
COPY . .
CMD ["ls"]
CMD ["python3", "src/main.py"]
