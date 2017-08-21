# Start with a Python image.
FROM python:latest

# Some stuff that everyone has been copy-pasting
# since the dawn of time.
ENV PYTHONUNBUFFERED 1

# Install some necessary things.
RUN apt-get update
RUN apt-get install -y swig libssl-dev dpkg-dev netcat

# Install all requirements
RUN pip install -U pip
ADD requirements.txt /code/
RUN pip install -Ur /code/requirements.txt

# Add the Dokku specific files to their locations
ADD misc/dokku/CHECKS /app/
ADD misc/dokku/* /code/

# Copy all our files into the image and collect staticfiles
WORKDIR /code
COPY . /code/
RUN python /code/manage.py collectstatic --noinput

