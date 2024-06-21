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

1. Create configuration file

    - copy `configs/config.json` to `configs-user/config.json`
    - set all values in `configs-user/config.json`
      - `serverName` - dns name of the server
      - set `serverName` in your DNS to point to the server

2. Create secrets
    TODO: Change that
    - change default passwords in files in `secrets` folder

3. Run database

    - `docker compose up -d database`

4. Start setup of default Root CA
      
    - Step 1 from [Root CA](/docs/root-ca.md#initial-steps) 

5. Setup Intermediate CA - this CA will be used to issue certificates used in all PKI, like OCSP, TLS, etc.

    - Do [Intermediate CA](/docs/intermediate-ca.md#initial-steps)


6. End setup of Root CA

    - Next steps from [Root CA](/docs/root-ca.md#initial-steps)

7. Start it 

    - `docker compose up -d`
  
8. Now you have fully working PKI with Root CA, and Intermediate CA.
  
      - Look for stepCA documentation to manage certificates. [Step CLI](https://smallstep.com/docs/step-cli/)
      - Intermediate CA endpoint is available at `https://<name>.<serverName>/` where `<name>` is the name of the Intermediate CA.
      - You can add more Root CAs and Intermediate CAs:
        - [Root CA](/docs/root-ca.md#initial-steps)
        - [Intermediate CA](/docs/intermediate-ca.md#initial-steps)
