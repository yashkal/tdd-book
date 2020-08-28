# Get official python image
FROM python:3.8.0-alpine

# Set the container working directory
WORKDIR /usr/src/app

# Prevents writing pyc files and buffering stdout and stderr
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /usr/src/app
RUN pip install --upgrade pip && \
pip install -r requirements.txt

COPY . /usr/src/app/

RUN chmod +x /usr/src/app/entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
