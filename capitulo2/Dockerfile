FROM python:3.13-slim

# Evita que Python genere archivos .pyc y carpetas __pycache__
ENV PYTHONDONTWRITEBYTECODE=1

# Envía inmediatamente los logs a la salida del contenedor
ENV PYTHONUNBUFFERED=1

# Directorio raíz del microservicio
WORKDIR /microservice

# Se copia primero para aprovechar la caché de Docker
COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt


# Usuario y grupo con IDs conocidos
RUN groupadd --system --gid 10001 appgroup \
    && useradd \
        --system \
        --uid 10001 \
        --gid 10001 \
        --create-home \
        --home-dir /home/appuser \
        appuser


# Copia la carpeta app como /microservice/app
COPY --chown=10001:10001 app ./app

# Directorio donde Kubernetes montará el volumen
RUN mkdir -p /data \
    && chown -R 10001:10001 /data

# main.py y los paquetes quedan disponibles desde este directorio
WORKDIR /microservice/app

# Ejecuta el proceso con el usuario sin privilegios
USER 10001:10001

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]