# start by pulling the python image 
FROM python:3.9-slim

# Set and create the working directory to /app 
WORKDIR /app

# copy the requirements file to speed up the building process
COPY requirements.txt /app

# install the dependencies and packages in the requirements file
RUN apt-get -y update
RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the current directory contents into /app 
COPY . /app

EXPOSE 8080

CMD ["gunicorn", "--workers=2", "--bind=0.0.0.0:8080", "main:app"]