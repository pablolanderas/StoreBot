FROM python:3.10-slim

RUN mkdir -p /app

COPY . /app

RUN pip install --no-cache-dir -r /app/dsg/dependencies.txt

CMD ["python", "/app/src/__main__.py"]