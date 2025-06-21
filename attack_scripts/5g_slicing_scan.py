#!/usr/bin/env python3
# Descripción: Detecta slices de red 5G con configuración insegura
import nmap

def scan_slices(target_ip):
    nm = nmap.PortScanner()
    nm.scan(target_ip, arguments='-p 38412 --script 5g-slice-info')
    
    for host in nm.all_hosts():
        print(f"\n[+] Slice IDs en {host}:")
        for script in nm[host]['scripts']:
            if "5g-slice-info" in script:
                print(f"  - {script['slice_id']} (QoS: {script['qos']})")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("target", help="IP del core 5G")
    args = parser.parse_args()
    scan_slices(args.target)
