ARG BUILD_FROM=ghcr.io/home-assistant/aarch64-base-python:3.12-alpine3.19
FROM $BUILD_FROM

# System-Abhängigkeiten
RUN apk add --no-cache \
    i2c-tools \
    build-base \
    python3-dev \
    jpeg-dev \
    zlib-dev \
    freetype-dev \
    lcms2-dev \
    openjpeg-dev \
    tiff-dev

WORKDIR /app

# Python-Pakete installieren
COPY requirements.txt .
RUN pip3 install --no-cache-dir --break-system-packages -r requirements.txt

# Skript und Starter kopieren
COPY display.py .
COPY run.sh /
RUN chmod a+x /run.sh

# Start-Befehl
CMD [ "/run.sh" ]
