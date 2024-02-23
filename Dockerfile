FROM python:3.12-slim

WORKDIR /app

ADD requirements.txt /app

RUN pip install --no-cache-dir -r requirements.txt

ADD . /app

EXPOSE 8000

CMD ["python", "server.py"]