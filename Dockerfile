FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    FLASK_ENV=production

WORKDIR /app

COPY requirements.txt .
RUN python -m pip install --upgrade pip setuptools wheel \
  && pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y sqlite3 && rm -rf /var/lib/apt/lists/*

COPY . .

RUN mkdir -p /app/instance && chmod -R 775 /app/instance

EXPOSE 5000

CMD ["gunicorn","--preload", "-b", "0.0.0.0:5000", "--workers", "1", "--threads", "2", "--timeout", "120", "wsgi:application"]
