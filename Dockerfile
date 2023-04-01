# Use the official lightweight Python image.
FROM python:3.11-slim

ENV APP_HOME /app
WORKDIR $APP_HOME

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PORT 8080

ENV DATABASE_URL $_DATABASE_URL
ENV SECRET_KEY $_SECRET_KEY

# Cambiar en la varaible de entorno de cloudbuild. Configuracion local
ENV DATABASE_URL postgresql://truefaces:truefaces@db:5432/truefaces

# install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .

CMD exec gunicorn --bind :$PORT --workers 1 --worker-class uvicorn.workers.UvicornWorker --threads 8 app.main:app
# CMD exec 'uvicorn app.main:app --host 0.0.0.0 --port 8080
