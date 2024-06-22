# Root CA

This guide will show you how to create a Root CA and add it to your PKI system.
System can have multiple Root CAs, for each CA you repeat the steps below.

## Initial steps

1. Generate new Root CA key and certificate

    I use here "The secure way" from [Step CA](https://smallstep.com/docs/tutorials/intermediate-ca-new-ca/) to create the Root CA and Intermediate CA.

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

2. Create intermediate CA

    Follow the steps in [Intermediate CA](./intermediate-ca.md) to create an Intermediate CA.

3. Configure Docker

    1. Run `python scripts root-ca <name> --intCa <intCa>`

        Where `<name>` is the name of the Root CA that will be used in the system. Should be simple and unique. Only letters, numbers and "-" are allowed.
        And `<intCa>` is the name of the Intermediate CA created in step 2. 

    2. Add new include to `docker-compose.yml`, path will be in output of step 4.1
        ```yaml
        include:
          - project_directory: ./
            path: 
              - ./docker-main.yml
              ...
              - ./configs/test/root-ca.yml
              ...
        ```

4. Generate CRL

    See [Update CRL and OCSP](#update-crl-and-ocsp) for more information.
    Do not do last step. Not restart the OCSP container.

5. Add files to config in `data/volumes/<name>/ocsp-data/`

    - `ca.crt` is the CA certificate from step 1, this file shoud have 644 permissions
    - `index.txt` file created in step 3
    - `index.txt.attr` file with content `unique_subject=no` if you want to allow multiple certificates with the same subject or `unique_subject=yes` if you want to allow only one certificate with the same subject

6. Generate proxy and OCSP certificates

    - Run `python scripts generate-proxy-certs <name>`
    - Run `python scripts generate-ocsp-certs <name>`

7. Add CNAME to DNS for `<name>.<serverName>` as `<serverName>`.

8. Restart the system

    Run `docker compose up -d`


## Update CRL and OCSP

On client copy `root-ca` folder from repository and go to it.

1. Run `python format-cert.py <intermediate-file-name>`

    Where `<intermediate-file-name>` is the name of the Intermediate CA created in step 2. 

2. Run `openssl ca -gencrl -config openssl.conf -cert <root-ca-cert> -keyfile <root-ca-key> -out crl.crt`
    Where `<root-ca-cert>` is the root CA certificate from step 1 and `<root-ca-key>` is the root CA key from step 1.

3. Copy `crl.crt` to `data/configs/<name>/crl.crt`
4. Copy `index.txt` to `data/volumes/<name>/ocsp-data/index.txt`
5. Restart ocsp container

    Run `docker compose restart <name>-ocsp`