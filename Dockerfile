FROM python:3.11-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN apt-get update && \
    apt-get install -y \
    netcat-openbsd \
    wget \
    gnupg \
    unzip \
    chromium \
    chromium-driver && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN chromium --version && \
    chromedriver --version

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PATH="/usr/lib/chromium:$PATH"
