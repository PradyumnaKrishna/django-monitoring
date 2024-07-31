FROM python:3.9-slim

# Port used by this container to serve HTTP.
EXPOSE 8000

# Set environment variables.
# 1. Force Python stdout and stderr streams to be unbuffered.
# 2. Set PORT variable that is used by Gunicorn. This should match "EXPOSE"
#    command.
ENV PYTHONUNBUFFERED=1 \
    PORT=8000

# Install required system packages.
RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
supervisor \
&& rm -rf /var/lib/apt/lists/*

# Install the application server.
RUN pip install "gunicorn==20.0.4"

# Install the project requirements.
COPY requirements.txt /
RUN pip install -r /requirements.txt

# Use /app folder as a directory where the source code is stored.
WORKDIR /app

# Copy the source code of the project into the container.
COPY django-monitoring /app

COPY docker/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Run the application
CMD ["/usr/bin/supervisord"]
