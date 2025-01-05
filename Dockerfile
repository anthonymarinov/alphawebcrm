FROM python:3.10-slim

# Install system deps
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        pkg-config \
        libmariadb-dev-compat \
        libmariadb-dev && \
    rm -rf /var/lib/apt/lists/*

# Create a non-root user
RUN useradd -m appuser

# Create /app and make it the working directory
WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt /app/

# Upgrade pip & install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the rest of code
COPY . /app/

# --- CREATE AND CHOWN THE STATICFILES DIR ---
RUN mkdir -p /app/staticfiles
RUN chown -R appuser:appuser /app

# Run collectstatic as appuser
USER appuser
# RUN python manage.py collectstatic --noinput

# Switch back to root
USER root

# (optionally) chown again if you changed stuff as root 
# RUN chown -R appuser:appuser /app

# Expose port and set final command
EXPOSE 8000
CMD gunicorn alphacrm.wsgi:application --bind 0.0.0.0:8000
