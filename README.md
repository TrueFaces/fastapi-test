# Docker:

## Local
Se añadido el docker-compose (poisblemente sea necesario instalar el paquete) porque así se se puede montar la aplicación web y la BD's en postgres de forma local

### Construir la imagen
    docker-compose build

### Ejecutar el contenedor
    docker-compose up
    
# GCP
Los depliegues han sido automatizados con Cloud Build


# CloudBuild
Se crea el fichero cloudbuild.yaml con los pasos del despliegue. Para que funcione correctamente hay que declarar dentro del trigger de despliegue las siguientes variables de entorno:
  _DATABASE_URL: postgresql://<usuario>:<password>@<ip de la bds>/<nombre del bds>
  _SECRET_KEY: Cadena alfanumérica para poder encriptar/desencriptar las contraseñas de los usuarios
  _BUCKET: Nombre del bucket en el que se almacenaran los datos de la aplicación
  
Se puede usar como ejemplo las variables definidas dentro del cloudbuild.yml

# Swagger (Documentación API)
Se ha montado dentro del proyecto un API con Swagger totalmente operativa. Se encuentra activa dentro de la ruta /docs

También se dispone la documentación en ReDoc en la ruta /redoc