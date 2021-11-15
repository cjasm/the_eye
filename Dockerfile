FROM python:3.8-alpine

# Setup container dependencies
RUN apk update && apk --no-cache --update add build-base
RUN apk add --update alpine-sdk libxml2-dev libxslt-dev openssl-dev libffi-dev zlib-dev musl-dev gcc python3-dev rust rustup cargo

# Adding The Eye Project
COPY . /the_eye
WORKDIR /the_eye
RUN rm -rf static/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENV SECRET_KEY ''
ENV ALLOWED_HOSTS ''

CMD python manage.py collectstatic --noinput && \
    python manage.py migrate && \
    gunicorn theeye.wsgi -w3 -t 1000 -b 0.0.0.0:8000