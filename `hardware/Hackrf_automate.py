import os
import time

def jam_5g(freq="3500M", duration=10):
    print(f"[+] Bloqueando {freq} por {duration}s...")
    os.system(f"hackrf_transfer -f {freq} -s 2000000 -n {duration*1000000}")

if __name__ == "__main__":
    jam_5g(freq="3500M", duration=5)
