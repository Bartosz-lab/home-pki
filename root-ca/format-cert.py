#!/usr/bin/python

import sys

from OpenSSL import crypto

if len(sys.argv) != 3:
    print("Usage: format-cert.py <cert-file> <index-file>")
    sys.exit(1)

certFile = sys.argv[1]
indexFile = sys.argv[2]

with open(certFile, "r") as f:
    data = f.read()

cert = crypto.load_certificate(crypto.FILETYPE_PEM, data)

notAfter = cert.get_notAfter().decode("utf-8")[2:]

serial = format(cert.get_serial_number(), "X")
dn = "".join(
    [
        f"{x[0].decode('utf-8')}={x[1].decode('utf-8')}"
        for x in cert.get_subject().get_components()
    ]
)

with open(indexFile, "a") as f:
    f.write(f"V\t{notAfter}\t\t{serial}\tunknown\t{dn}\n")
