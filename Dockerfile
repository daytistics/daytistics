FROM python:3.12-slim

WORKDIR /app

RUN pip install poetry

RUN apt-get update && \
    apt-get install -y nodejs npm

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root

COPY theme/package*.json ./theme/
RUN cd theme && npm install

COPY . .

RUN cd theme && npm run build

EXPOSE 8000

CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
