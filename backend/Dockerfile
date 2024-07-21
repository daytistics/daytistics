# Use an official Python runtime as a parent image
FROM python:3.12.4-slim

# Set the working directory in the container
WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y curl

# Ensure pip is installed and upgraded to the latest version
RUN apt-get install -y python3-pip
RUN pip install --no-cache-dir --upgrade pip

# Install Poetry using the official installation script
RUN curl -sSL https://install.python-poetry.org | python3 -

# Ensure the Poetry binary is in the PATH
ENV PATH="/root/.local/bin:$PATH"

# Configure Poetry to create the virtual environment inside the project directory
RUN poetry config virtualenvs.in-project true

# Copy only the files needed for Poetry to install dependencies
COPY poetry.lock pyproject.toml /app/

# Install dependencies
RUN poetry install --no-root

# Copy the rest of the application code
COPY src /app/src
COPY config.py /app/config.py
COPY .env /app/.env

# Expose the port Flask will run on
EXPOSE 5000

# Run the Flask app
CMD ["poetry", "run", "flask", "run", "--host=0.0.0.0"]
