#!/usr/bin/env python3
# Descripción: Encuentra dispositivos IoT 5G con configuraciones inseguras
import requests

TARGETS = [
    "industrial-iot-5g", 
    "smart-meter",
    "medical-iot"
]

def scan_iot(target):
    try:
        r = requests.get(f"http://{target}/api/v1/config", timeout=3)
        if r.status_code == 200 and "password" in r.text:
            print(f"[!] {target}: Configuración expuesta (API)")
    except Exception as e:
        pass

for device in TARGETS:
    scan_iot(device)
