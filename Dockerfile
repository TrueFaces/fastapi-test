# Use the official lightweight Python image.
FROM python:3.9-slim

ENV APP_HOME /app
WORKDIR $APP_HOME

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PORT 8080

# install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .