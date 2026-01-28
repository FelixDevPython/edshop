# -------------------------------
# Imagen base
# -------------------------------
FROM python:3.9.6-alpine

# -------------------------------
# Configurar directorio de trabajo
# -------------------------------
WORKDIR /usr/src/app

# -------------------------------
# Variables de entorno
# -------------------------------
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# -------------------------------
# Instalar dependencias del sistema
# -------------------------------
RUN apk add --update --no-cache \
        mariadb-connector-c-dev \
        libffi-dev \
        openssl-dev \
        bash \
        build-base \
        linux-headers

# -------------------------------
# Instalar pip y dependencias Python
# -------------------------------
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# -------------------------------
# Copiar todo el proyecto
# -------------------------------
COPY . .

# -------------------------------
# Comando por defecto
# -------------------------------
CMD ["gunicorn", "edshop.wsgi:application", "--bind", "0.0.0.0:8000"]
