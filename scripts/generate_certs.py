import subprocess
import os
import shutil


def generateProxyCert(mainConfig, caName, intermediateCaName=None):
    print("Generating proxy certificate")
    serverName = f"{caName}.{mainConfig['serverName']}"

    if intermediateCaName is None:
        intermediateCaName = caName

    subprocess.run(
        [
            "docker",
            "compose",
            "run",
            "--rm",
            "-v",
            f"{os.getcwd()}/data/volumes/{caName}/proxy-certs:/proxy",
            f"{intermediateCaName}-ca",
            "step",
            "ca",
            "certificate",
            serverName,
            "/proxy/cert.crt",
            "/proxy/cert.key",
        ],
    )
    print("Proxy certificate generated")


def generateOCSPCert(mainConfig, caName, certName=None):
    print("Generating OCSP certificate")

    if certName is None:
        certName = f"{caName} OCSP"

    shutil.copy(
        f"data/configs/{caName}/ca/certs/intermediate_ca.crt",
        f"data/volumes/{caName}/ocsp-certs/ca.crt",
    )

    # TODO: This should be special certificate for OCSP
    subprocess.run(
        [
            "docker",
            "compose",
            "run",
            "--rm",
            "-v",
            f"{os.getcwd()}/data/volumes/{caName}/ocsp-certs:/ocsp",
            f"{caName}-ca",
            "step",
            "ca",
            "certificate",
            certName,
            "/ocsp/ocsp.crt",
            "/ocsp/ocsp.key",
        ],
    )
    print("OCSP certificate generated")


def generateOCSPCertForRootCA(mainConfig, caName, intermediateCaName, certName=None):
    print("Generating OCSP certificate")

    if certName is None:
        certName = f"{caName} OCSP"

    # TODO: This should be special certificate for OCSP
    subprocess.run(
        [
            "docker",
            "compose",
            "run",
            "--rm",
            "-v",
            f"{os.getcwd()}/data/volumes/{caName}/ocsp-data:/ocsp",
            f"{intermediateCaName}-ca",
            "step",
            "ca",
            "certificate",
            certName,
            "/ocsp/ocsp.crt",
            "/ocsp/ocsp.key",
        ],
    )
    print("OCSP certificate generated")
