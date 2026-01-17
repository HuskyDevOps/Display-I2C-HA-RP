from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from PIL import Image, ImageDraw, ImageFont
import psutil
import time
import requests
import os
import logging

# Logging einrichten
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logging.info("Display-Skript startet...")

# I2C Display
serial = i2c(port=1, address=0x3C)
device = ssd1306(serial, width=128, height=64)

font_small = ImageFont.load_default()

SUPERVISOR_TOKEN = os.getenv("SUPERVISOR_TOKEN")
SUPERVISOR_URL = "http://supervisor/info"

def get_cpu_temp():
    try:
        with open("/sys/class/thermal/thermal_zone0/temp") as f:
            return int(f.read()) / 1000.0
    except Exception as e:
        logging.error(f"Fehler beim Lesen der CPU-Temperatur: {e}")
        return 0.0

def get_ha_status():
    try:
        headers = {"Authorization": f"Bearer {SUPERVISOR_TOKEN}"}
        r = requests.get(SUPERVISOR_URL, headers=headers, timeout=2)
        data = r.json()
        return data.get("data", {}).get("state", "unknown")
    except Exception as e:
        logging.error(f"Fehler beim Lesen des HA-Status: {e}")
        return "error"

blink_state = False
last_blink = time.time()
blink_interval = 0.5

last_update = 0
update_interval = 1.0

cpu = ram = temp = 0.0
ha_status = "?"

while True:
    now = time.time()

    if now - last_blink >= blink_interval:
        blink_state = not blink_state
        last_blink = now

    if now - last_update >= update_interval:
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        temp = get_cpu_temp()
        ha_status = get_ha_status()
        last_update = now

        logging.info(f"CPU={cpu:.1f}% RAM={ram:.1f}% Temp={temp:.1f}°C HA={ha_status}")

    img = Image.new("1", (128, 64), 0)
    draw = ImageDraw.Draw(img)

    # Kopfzeile
    draw.text((0, 0), "System Monitor", font=font_small, fill=255)

    # Werte
    draw.text((0, 14), f"CPU: {cpu:4.1f}%", font=font_small, fill=255)
    draw.text((0, 26), f"RAM: {ram:4.1f}%", font=font_small, fill=255)
    draw.text((0, 38), f"Temp: {temp:4.1f}C", font=font_small, fill=255)
    draw.text((0, 50), f"HA: {ha_status}", font=font_small, fill=255)

    # Balken
    bar_x = 70
    bar_width = 50
    bar_height = 6

    cpu_bar = int(bar_width * cpu / 100)
    ram_bar = int(bar_width * ram / 100)

    draw.rectangle((bar_x, 16, bar_x + bar_width, 16 + bar_height), outline=255)
    draw.rectangle((bar_x, 16, bar_x + cpu_bar, 16 + bar_height), fill=255)

    draw.rectangle((bar_x, 28, bar_x + bar_width, 28 + bar_height), outline=255)
    draw.rectangle((bar_x, 28, bar_x + ram_bar, 28 + bar_height), fill=255)

    # HA Status LED
    led_x = 120
    led_y = 54
    r = 4

    if ha_status == "running":
        fill = 255
    else:
        fill = 0

    draw.ellipse((led_x-r, led_y-r, led_x+r, led_y+r), outline=255, fill=fill)

    device.display(img)
    time.sleep(0.05)