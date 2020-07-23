# Get official python image
FROM python:3.8.0-alpine

# Set the container working directory
WORKDIR /usr/src/app

# Prevents writing pyc files and buffering stdout and stderr
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV DEBUG 1
ENV SECRET_KEY foo
ENV DJANGO_ALLOWED_HOSTS localhost 127.0.0.1 [::1]

RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app
RUN pip install -r requirements.txt

COPY . /usr/src/app/

CMD python3 manage.py runserver 0.0.0.0:8000
