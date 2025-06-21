#!/bin/bash
# Configura gNodeB falso con srsRAN
set -e

# Variables editables
PLMN="00101"
FREQ="3680M"

echo "[+] Configurando gNodeB en $FREQ..."
srsenb --plmn=$PLMN --dl_earfcn=$FREQ --n_prb=50 --tx_gain=80
