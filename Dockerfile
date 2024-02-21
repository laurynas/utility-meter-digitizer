FROM python:3.11-slim-bookworm

WORKDIR /app

ADD Pipfile* /app

RUN pip install --no-cache-dir pipenv && pipenv install --system --deploy

ADD . /app

EXPOSE 8000

CMD ["python", "server.py"]