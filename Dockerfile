FROM python:3-slim
WORKDIR /app

EXPOSE 5000
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN apt-get update && apt-get install -y gcc libpq-dev && \
    python -m pip install --upgrade pip && \
    python -m pip install -r requirements.txt

COPY . /app
CMD ["gunicorn", "--bind", "0.0.0.0:8081", "app:app"]
