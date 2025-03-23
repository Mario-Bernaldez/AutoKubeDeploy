# Usamos una imagen base de Python
FROM python:3.12-slim

# Configurar variables de entorno
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8000

# Crear y establecer el directorio de trabajo
WORKDIR /app

# Copiar archivos de dependencias
COPY kube-web/requirements.txt /app/requirements.txt

# Instalar dependencias
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar el resto de la aplicación
COPY . /app/

# Crear la carpeta para archivos estáticos y migraciones
RUN mkdir -p /app/static && \
    python manage.py collectstatic --noinput && \
    python manage.py migrate

# Exponer el puerto en el que corre Django
EXPOSE 8000

# Comando para ejecutar la aplicación con Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "kube-web.wsgi:application"]
