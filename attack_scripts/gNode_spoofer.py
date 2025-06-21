#!/usr/bin/env python3
# Descripción: Emulador básico de gNodeB para pruebas de seguridad

import subprocess
import argparse

def spoof_gNodeB(plmn="00101", tac=7, dl_freq=3680.0e6):
    """
    Simula una estación base 5G con srsRAN
    Args:
        plmn (str): Código de red móvil (ej: 00101)
        tac (int): Código de área de tracking
        dl_freq (float): Frecuencia downlink en Hz
    """
    config = f"""
[enb]
plmn = {plmn}
tac = {tac}
dl_earfcn = {int(dl_freq/1e6)}
"""
    
    with open("spoofed_gnb.conf", "w") as f:
        f.write(config)
    
    print(f"[+] Iniciando gNodeB falso en {dl_freq/1e6} MHz")
    subprocess.run(["srsenb", "spoofed_gnb.conf"], check=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--plmn", default="00101", help="PLMN ID (ej: 00101)")
    parser.add_argument("--freq", type=float, default=3680.0, 
                       help="Frecuencia en MHz (ej: 3680.0)")
    args = parser.parse_args()
    
    spoof_gNodeB(plmn=args.plmn, dl_freq=args.freq * 1e6)
