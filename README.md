# home-pki

PKI based on step-ca, postgres and docker with ocsp


## Endpoints
I use here `pki.example.com` as a domain name. You should replace it with your domain name. `root` as a name of the Root CA, and `int1` as a name of the Intermediate CA.

- Root CA
  - `https://pki.example.com/root/ca` Root CA Certificate
  - `http://pki.example.com/root/ocsp` OCSP Responder
  - `http://pki.example.com/root/crl` CRL

- Intermediate CA
  - `https://pki.example.com/int1/` Endpoint for StepCA
  - `http://pki.example.com/int1/ocsp` OCSP Responder
  - `http://pki.example.com/int1/crl` CRL


## Initial Setup

1. Create configuration file

    - copy `configs/config.json` to `configs-user/config.json`
    - set all values in `configs-user/config.json`
      - `serverName` - dns name of the server
      - `defaultIntermediateCA` - name of the default Intermediate CA, CA with this name should be created in step 5

2. Create secrets
    TODO: Change that
    - change default passwords in files in `secrets` folder

3. Run database

    - `docker compose up -d database`

4. Start setup of default Root CA
      
    - Step 1 from [Root CA](/docs/root-ca.md#initial-steps) 

5. Setup Intermediate CA - this CA will be used to issue certificates used in all PKI, like OCSP, TLS, etc.

    - Do [Intermediate CA](/docs/intermediate-ca.md#initial-steps)


6. Generate certificate for Proxy

    - Run `python scripts generate-proxy-certs`
    - When asked provide password for default StepCA provisioner - on start it same as password for private key of intermediate CA

7. End setup of Root CA

    - Next steps from [Root CA](/docs/root-ca.md#initial-steps)

8. Start it 

    - `docker compose up -d`
  
9. Now you have fully working PKI with Root CA, and Intermediate CA.
  
      - Look for stepCA documentation to manage certificates. [Step CLI](https://smallstep.com/docs/step-cli/)
      - Intermediate CA sends is `<serverName>/,defaultIntermediateCA.` - see [Endpoint](#endpoints)
      - You should change default change password for default StepCA provisioner. \
        It will be used to generate certificates used by this PKI system for internal purposes eg. adding new CAs. \
        See [StepCA Replace default provisioner](https://smallstep.com/docs/step-ca/certificate-authority-server-production/#replace-your-default-provisioner)
      - You can add more Root CAs and Intermediate CAs:
        - [Root CA](/docs/root-ca.md#initial-steps)
        - [Intermediate CA](/docs/intermediate-ca.md#initial-steps)
