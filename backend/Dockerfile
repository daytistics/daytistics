# Replace with the latest Python version
FROM python:3.12

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DJANGO_SETTINGS_MODULE=daytistics.config.settings.prod

# Set the working directory
WORKDIR /app

RUN python --version

# Install Node.js and npm
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs

# Install dependencies for MariaDB
RUN apt-get update && \
    apt-get install -y python3-dev default-libmysqlclient-dev build-essential pkg-config

# Install Poetry
RUN pip install poetry

# Copy pyproject.toml and poetry.lock
COPY pyproject.toml poetry.lock /app/

# Configure Poetry to not use virtualenvs
RUN poetry config virtualenvs.create false

# Install Python dependencies
RUN poetry install --no-dev --no-root

# Copy the entire project
COPY . /app/

# Install Tailwind CSS (requires Node.js and npm)
RUN python manage.py tailwind install --no-input;

# Build Tailwind CSS
RUN python manage.py tailwind build --no-input;

# Collect static files
RUN python manage.py collectstatic --no-input;

# Make migrations
RUN python manage.py makemigrations --no-input;

# Migrate the database
RUN python manage.py migrate --no-input;

# Expose port 8000
EXPOSE 8000

# Start the application with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]