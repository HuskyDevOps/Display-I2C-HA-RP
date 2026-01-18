ARG BUILD_FROM=ghcr.io/home-assistant/aarch64-base:latest
FROM $BUILD_FROM

# Installiere System-Abhängigkeiten und Build-Tools
RUN apk add --no-cache \
    python3 \
    py3-pip \
    i2c-tools \
    # Notwendig zum Kompilieren von Python-Modulen (z.B. Pillow oder SMBus)
    build-base \
    python3-dev \
    # Grafik-Bibliotheken für Pillow (I2C Displays brauchen oft Bilder/Fonts)
    jpeg-dev \
    zlib-dev \
    freetype-dev \
    lcms2-dev \
    openjpeg-dev \
    tiff-dev

WORKDIR /app

# Kopiere Anforderungen und installiere sie
# --break-system-packages ist in neueren Alpine/Python-Versionen oft nötig
COPY requirements.txt .
RUN pip3 install --no-cache-dir --break-system-packages -r requirements.txt

# Kopiere das Skript
COPY display.py .

# Starte das Skript
CMD [ "python3", "/app/display.py" ]
