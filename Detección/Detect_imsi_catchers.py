#!/usr/bin/env python3
# Detecta posibles IMSI Catchers en redes 5G

from scapy.all import sniff
from scapy.layers.ngap import NGAP

def analyze_packet(pkt):
    if pkt.haslayer(NGAP):
        # Regla básica: PLMN sospechoso o TAC no registrado
        if pkt.plmn_id == "99999":  # PLMN de prueba/reservado
            print(f"[!] Posible IMSI Catcher detectado: PLMN={pkt.plmn_id}")

print("[*] Monitoreando tráfico NGAP...")
sniff(iface="any", filter="port 38412", prn=analyze_packet)
