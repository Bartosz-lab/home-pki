# home-pki

PKI based on step-ca, postgres and docker with ocsp


## Endpoints
I use here `pki.example.com` as a domain name. You should replace it with your domain name. `root` as a name of the Root CA, and `int1` as a name of the Intermediate CA.

- Root CA
  - `https://root.pki.example.com/ca` Root CA Certificate
  - `http://root.pki.example.com/ocsp` OCSP Responder
  - `http://root.pki.example.com/crl` CRL

- Intermediate CA
  - `https://int1.pki.example.com/` Endpoint for StepCA
  - `http://int1.pki.example.com/ocsp` OCSP Responder
  - `http://int1.pki.example.com/crl` CRL


## Initial Setup

1. Create configuration
    - run `python scripts generate-data-dir`
    - set all values in `data/config.json`
      - `serverName` - dns name of the server
      - set `serverName` in your DNS to point to this server

2. Create secrets
    - change default database password in `data/secrets/db-password.txt`

3. Start default services

    - `docker compose up -d`

4. Setup first Root CA and Intermediate CA
      
    - [Root CA](/docs/root-ca.md#initial-steps) 
    - [Intermediate CA](/docs/intermediate-ca.md#initial-steps)

    > [!IMPORTANT]
    > Remember to update `docker-compose.yml` with new services.
    > Remember to restart the services after changes.

5. Now you have fully working PKI with Root CA, and Intermediate CA.
  
      - Look for stepCA documentation to manage certificates. [Step CLI](https://smallstep.com/docs/step-cli/)
      - Look for [Endpoints](#endpoints) to see where you can find stepCA server, OCSP and CRL.
      - You can add more Root CAs and Intermediate CAs:
        - [Root CA](/docs/root-ca.md#initial-steps)
        - [Intermediate CA](/docs/intermediate-ca.md#initial-steps)


## Remove services for specific CA

1. remove include from `docker-compose.yml`

2. remove files from `data/configs/<name>` and `data/volumes/<name>`

3. restart services

  Run `docker compose up -d --remove-orphans`

4. remove database
  
  You should remove database manually. You can use ` docker compose exec -it database psql -U postgres` and then `DROP DATABASE "<name>"; DROP USER "<name>";`

5. If you remove intermediate CA, you should update Root CA with new CRL and OCSP data.

  - [Root CA](/docs/root-ca.md#update-crl-and-ocsp)
  

## Backup 

- `python scripts backup`
- backup will be saved in `backup/backup-pki.tar.gz`
- script do not backup certificates and keys for proxy and ocsp. You should regenerate them after restore.




## Limitations

- System is not ready for production use.
- You can't use mtls to renew certificates. When you use `step ca renew` you need to provide `--mtls=false` flag.

## Known issues  
  - `root-ca/format-cert` cuts leading zeros in serial number. 