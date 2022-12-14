FROM python:3.8

ENV PYTHONUNBUFFERED 1

# Root directory in the container
RUN mkdir /MVP

# Set the working directory to /MVP
WORKDIR /MVP

# Create python virtual environment
RUN python3 -m venv venv

# Activate virtual environment
RUN . venv/bin/activate

ADD ./requirements.txt /MVP/requirements.txt

# Install dependencies
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /MVP
ADD . /MVP

RUN apt-get -q update && apt-get -qy install netcat

# Make wait-for-it.sh executable
RUN chmod +x ./wait-for.sh

COPY ./entrypoint.sh /

ENTRYPOINT ["sh", "/entrypoint.sh"]
