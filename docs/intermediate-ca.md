# Intermediate CA

## Initial steps

1. Gnerate new Intermediate CA key and certificate

    ```bash
    # On Server

    # Create file with password
    step crypto rand 40 > password
    # Create Intermediate CA CSR
    step certificate create "<Your Intermediate CA>" intermediate_ca.csr intermediate_ca.key --csr --password-file password
    # Send intermediate_ca.csr to client.
    ```

    ```bash
    # On Client

    24h*365d*10y=87660h = 10 years
    step certificate sign intermediate_ca.csr root_ca.crt root_ca.key --password-file root_ca_password.txt --not-after 87660h --template stepca/templates/intermediate.tpl --set-file stepca/templates/intermediate-data.json > intermediate_ca.crt
    # Send intermediate_ca.crt and root_ca.crt to server.

    # TODO: Add CRL and OCSP generation
    ```
2. Configure Docker
    
    1. Run `python scripts intermediate-ca <name>`
    
        Where `<name>` is the name of the Intermediate CA that will be used in the system. Should be simple and unique. Only letters, numbers and "-" are allowed.
    
    2. Add new include to `docker-compose.yml`, path will be in output of step 2.1
         ```yaml
        include:
            - path: 
              - ./docker-main.yml
              ...
              - ./data/configs/test/intermediate-ca.yml
              ...
            project_directory: ./
        ```
3. Configure database

    Run `docker compose exec database sh init.sh`, this will create the database and the user for the new Intermediate CA.

4. Add files to config

    1. Add `root_ca.crt` and `intermediate_ca.crt` to `data/configs/<name>/ca/certs/`
    2. Add `password` and `intermediate_ca.key` to `data/configs/<name>/ca/secrets/`

5. Run intermediate CA

    Run `docker compose up -d <name>-ca`

6. Generate OCSP certificate

    - Run `python scripts generate-ocsp-certs <name>`
    - When asked provide password for default StepCA provisioner - on start it same as password for private key of intermediate CA

> [!WARNING]
> If you configure default Intermediate CA, you should do additional steps from [Initial Setup](../README.md#initial-setup) before system restart and reconfiguring provisioner.

7. Restart the system

    TODO: Add restart


8. Delete or change password for default provisioner
    See [StepCA Replace default provisioner](https://smallstep.com/docs/step-ca/certificate-authority-server-production/#replace-your-default-provisioner)