# OCSP Responder for Root CA

This responder gets the revocation information from the static list provided by the user. 

## Volumes

- `/etc/ocsp/` is the volume with all the configuration files.
    - `ca.crt` is the CA certificate for the OCSP responder.
    - `ocsp.crt` is the OCSP certificate.
    - `ocsp.key` is the OCSP private key.
    - `index.txt` is the list of revoked certificates.