#!/bin/sh

inotifyd reboot /etc/ocsp/ocsp.crt:c &

openssl ocsp \
    -index /etc/ocsp/index.txt \
    -port 80 \
    -rsigner /etc/ocsp/ocsp.crt \
    -rkey /etc/ocsp/ocsp.key \
    -CA /etc/ocsp/ca.crt \
    -multi 4 \
    -timeout 3600 \
    -ignore_err