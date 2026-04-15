# 1. Imagen base Python 3.11 
FROM python:3.11-slim

# 2. Configuración del entorno de Python
# Evita que Python escriba archivos .pyc
ENV PYTHONDONTWRITEBYTECODE=1
# Evita que Python almacene en buffer stdout y stderr
ENV PYTHONUNBUFFERED=1

# 3. Directorio de trabajo dentro del contenedor
WORKDIR /app

# 4. Instalación de dependencias del sistema operativo para mysqlclient
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    mariadb-client \
    && rm -rf /var/lib/apt/lists/*

# 5. Gestión de dependencias de la aplicación
# Copia el archivo de requisitos
COPY requirements.txt /app/
# Instala las dependencias de Python
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 6. Integración del código fuente del proyecto
COPY . /app/

# 7. Preparación del sistema de archivos - Crea el directorio para archivos multimedia
RUN mkdir -p /app/media

# 8. Configuración de red - Expone el puerto 8000 (puerto por defecto de Django)
EXPOSE 8000

# 9. Punto de entrada (Comando de ejecución por defecto)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]