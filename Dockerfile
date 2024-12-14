FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    libcublaslt11 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
    
WORKDIR /app

ADD requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

ADD . /app

USER www-data
EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--access-logfile", "-", "app:app"]
