# Pull base image
FROM python:2.7

# Set env variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Set work directory
RUN mkdir /usr/src/app
WORKDIR /usr/src/app

# Add and ubsrakk
ADD /registration/requirements.txt /usr/src/app/
RUN pip install -r requirements.txt

# Copy project
ADD . /usr/src/app/