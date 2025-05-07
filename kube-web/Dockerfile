# Use a base Python image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8000

# Create and set the working directory
WORKDIR /app

# Copy dependency files
COPY kube-web/requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . /app/

# Create folder for static files and apply migrations
RUN mkdir -p /app/static && \
    python manage.py collectstatic --noinput && \
    python manage.py migrate

# Expose the port Django runs on
EXPOSE 8000

# Command to run the application with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--timeout", "60", "kube-web.wsgi:application"]
