# Docker:

## Local
### Construir la imagen
    docker build -t truefaces:1.0 .

### Ejecutar el contenedor
    docker run -d -p 8000:8000 --name truefaces truefaces:1.0

## GCP
### Construir imagen para el repositorio
    gcloud builds submit --tag gcr.io/{project_id}/{container_name}

Ejemplo:
    
    gcloud builds submit --tag gcr.io/kcbootcamp-380917/truefaces-api

### Desplegar imagen en Cloud Run
    gcloud run deploy --image gcr.io/{project_id}/{container_name} --platform managed

Ejemplo:

    gcloud run deploy --image gcr.io/kcbootcamp-380917/truefaces-api --platform managed
