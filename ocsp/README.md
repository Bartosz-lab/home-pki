# OCSP Responder

## Periodic Refresh

The OCSP responder periodically refreshes the OCSP database. The refresh can be done in two ways - full and incremental. The full refresh should be done at least once a day (see `CRON_REFRESH_FULL` configuration) and the incremental refresh should be done more frequently (see `CRON_REFRESH_INCREMENTAL` configuration). The full refresh is done by rebuilding the entire OCSP database, while the incremental refresh is done by updating the database with the new  and revoked certificates. 
WARNING: Scripts assumes that the step-ca database never deletes data and that the database responds with added order.


## Configuration

- `CRON_REFRESH_FULL`  is a cron format string that defines when the full refresh should be done. Default is `0 0 * * *` which means every day at midnight.
- `CRON_REFRESH_INCREMENTAL` is a cron format string that defines when the incremental refresh should be done. Default is `*/15 * * * *` which means every 15 minutes.
- `OCSP_NMIN` Number of minutes when fresh revocation information is available. Should be related to the `CRON_REFRESH_INCREMENTAL` configuration. Default is 15 minutes.

- `DB_HOST` is the hostname of the database. 
- `DB_PORT` is the port of the database, default is 5432.
- `DB_NAME` is the name of the database.
- `DB_USER` is the username of the database.
- `DB_PASSWORD` is the password of the database.

## Volumes

- `/usr/src/app/data` is the volume where the OCSP database is stored. This volume should be mounted to a persistent volume.
- `/usr/src/app/certs` is the volume where the OCSP responder stores the certificates. This volume should be mounted to a persistent volume.
    - `root_ca.crt` is the root CA certificate.
    - `ca.crt` is the CA certificate for the OCSP responder.
    - `ocsp.crt` is the OCSP certificate.
    - `ocsp.key` is the OCSP private key.