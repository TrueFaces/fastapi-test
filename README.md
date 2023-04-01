# Docker:

## Local
Se añadido el docker-compose porque así es capaza de montar la aplicación web y la BD's en postgres

### Construir la imagen
    docker-compose build

### Ejecutar el contenedor
    docker-compose up
    
## GCP
### Construir imagen para el repositorio
    gcloud builds submit --tag gcr.io/{project_id}/{container_name}

Ejemplo:
    
    gcloud builds submit --tag gcr.io/kcbootcamp-380917/truefaces-api

### Desplegar imagen en Cloud Run
    gcloud run deploy --image gcr.io/{project_id}/{container_name} --platform managed

Ejemplo:

    gcloud run deploy --image gcr.io/kcbootcamp-380917/truefaces-api --platform managed


## CloudBuild
Para realizar los despliegues de codigo automáticos

Se crea el fichero cloudbuild.yaml con los pasos del despliegue.