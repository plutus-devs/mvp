FROM python:3.8

ENV PYTHONUNBUFFERED 1

# Root directory in the container
RUN mkdir /MVP

# Set the working directory to /MVP
WORKDIR /MVP

# Copy the current directory contents into the container at /MVP
ADD . /MVP

# Create python virtual environment
RUN python3 -m venv venv

# Activate virtual environment
RUN . venv/bin/activate

# Install dependencies
RUN pip install -r requirements.txt

RUN apt-get -q update && apt-get -qy install netcat

# chmod +x wait-for.sh file
RUN chmod +x ./wait-for.sh



