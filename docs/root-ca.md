# Root CA

This guide will show you how to create a Root CA and add it to your PKI system.
System can have multiple Root CAs, for each CA you repeat the steps below.

## Initial steps

1. Generate new Root CA key and certificate

    I use here "The secure way" from [Step CA](https://smallstep.com/docs/tutorials/intermediate-ca-new-ca/) to create the Root CA and Intermediate CA.

    TODO: Change max path

    ```bash
    # On Client

    # Create file with password
    step crypto rand 40 > root_ca_password.txt
    # Create Root CA
    # 24h*365d*30y=262800h = 30 years
    step certificate create "<Your Root CA>" root_ca.crt root_ca.key --profile root-ca --not-after 262800h --password-file root_ca_password.txt
    ```

    > [!WARNING]
    > Please store the root_ca.key and root_ca_password.txt in a secure places.

    > [!IMPORTANT]
    > If this is the first CA in the system you should now [Create the Intermediate CA](./intermediate-ca.md).

2. Generate CRL

    TODO: Add CRL generation

3. Generate OCSP key and certificate

    TODO: Add OCSP generation

4. Configure Docker

    1. Run `python scripts/root-ca.py <name>`

        Where `<name>` is the name of the Root CA that will be used in the system. Should be simple and unique. Only letters, numbers and "-" are allowed.

    2. Add new include to `docker-compose.yml`, path will be in output of step 4.1
        ```yaml
        include:
          - path: 
              - ./docker-main.yml
              ...
              - ./configs/test/root-ca.yml
              ...
            project_directory: ./
        ```
    3. Add new volumes to `docker-compose.yml`  volumes names will be in output of step 4.1
        ```yaml
        volumes:
          ...
          test-ocsp-data:
          ...
        ```

5. Add data to ocsp volume

    1. `<NAME>-ocsp-data`
    
        - `ca.crt` is the CA certificate from step 1
        - `ocsp.crt` is the OCSP certificate from step 2
        - `ocsp.key` is the OCSP private key from step 2
        - `index.txt` is the list of revoked certificates - empty for now


## Update CRL and OCSP