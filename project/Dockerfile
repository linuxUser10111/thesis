# start by pulling the python image 
FROM python:3.9-slim

# Set and create the working directory to /app 
WORKDIR /app

# Copy the current directory contents into /app 
COPY . /app

# install the dependencies and packages in the requirements file
RUN apt-get -y update
RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip3 install --no-cache-dir -r requirements.txt

# Run app.py when the container launches
CMD ["python", "./main.py"]