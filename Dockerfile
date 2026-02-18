FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY .env .
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY worker.py .
COPY src ./src
COPY image ./image
CMD ["python", "worker.py"]



