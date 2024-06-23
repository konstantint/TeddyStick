# Wifi config (used in boot.py).
WIFI_SSID = "<YOUR WIFI SSID>"
WIFI_PASSWORD = "<YOUR WIFI PASSWORD>"

# MStickCPlus screen size.
SCREEN_WIDTH = 135
SCREEN_HEIGHT = 240

# TeddyCloud URL.
TEDDYCLOUD_URL = "http://<YOUR-TEDDYCLOUD-HOST>:7780"

# Tonies that can be configured. The images must be 135 x 180 JPGs.
TONIES = [
    {"img": "res/img/BerryCreativeTonie.jpg", "tag_id": "????????500304e0"},
    {"img": "res/img/FairyCreativeTonie.jpg", "tag_id": "????????500304e0"},
]

# List of sources to allow choosing from.
# 'url' can be anything that TeddyCloud understands (e.g lib:/ or http(s):/).
SOURCES = [
    {"title": "Local MPD", "url": "http://192.168.1.1:8000/"},
    {
        "title": "Energy Zurich",
        "url": "https://energyzuerich.ice.infomaniak.ch/energyzuerich-high.mp3",
    },
    {
        "title": "Radio SantaClaus",
        "url": "https://streaming.radiostreamlive.com/radiosantaclaus_devices",
    },
    # ... etc ...
]
