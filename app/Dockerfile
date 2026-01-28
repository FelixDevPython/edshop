# Imagen base
FROM python:3.9.6-alpine

# Directorio de trabajo
WORKDIR /usr/src/app

# Variables de entorno
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Dependencias del sistema
RUN apk add --update --no-cache mariadb-connector-c-dev \
    && apk add --no-cache --virtual .build-deps mariadb-dev gcc musl-dev \
    && pip install mysqlclient==1.4.2.post1 \
    && apk del .build-deps \
    && apk add libffi-dev openssl-dev libgcc bash

# Actualizar pip e instalar dependencias Python
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copiar todo el proyecto
COPY . .

# Exponer el puerto (Render usa 8000 por defecto)
EXPOSE 8000

# Comando para correr Django con Gunicorn
CMD ["gunicorn", "edshop.wsgi:application", "--bind", "0.0.0.0:8000"]

