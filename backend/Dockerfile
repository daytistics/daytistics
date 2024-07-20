FROM python:3.12.4

RUN poetry config virtualenvs.in-project true


RUN pip install poetry

COPY .venv /app
COPY src /app
COPY config.py /app
COPY poetry.lock /app
COPY pyproject.toml /app
COPY .env /app

RUN poetry install

CMD [ "poetry", "run", "flask", "run" ]