# Use the official lightweight Python image.
FROM python:3.11-slim

ENV APP_HOME /app
WORKDIR $APP_HOME

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV GOOGLE_APPLICATION_CREDENTIALS $APP_HOME/secrets/service_account.json

# install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .
# COPY modelo.h5 $APP_HOME/

CMD exec gunicorn --workers 1 --worker-class uvicorn.workers.UvicornWorker --threads 1 app.main:app
# CMD exec 'uvicorn app.main:app --host 0.0.0.0 --port 8080
