#!/usr/bin/with-contenv bashio

echo "--- I2C Bus Scan ---"
# Scannt den Bus 1 und gibt die Matrix im Log aus
i2cdetect -y 1 || echo "I2C-Tools nicht gefunden oder Bus belegt"

echo "Starte I2C Display Skript..."
cd /app
python3 display.py
