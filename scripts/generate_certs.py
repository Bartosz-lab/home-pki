import subprocess
import os
import shutil

from helpers import DirOperations, readConfigFile
from config import DefaultFileLocations


def generateProxyCert(mainConfig, caName):
    print("Generating proxy certificate")

    serverName = f"{caName}.{mainConfig['serverName']}"

    conf = readConfigFile(f"{DefaultFileLocations.configDir}/{caName}/config.json")
    if conf["type"] == "root-ca":
        intermediateCaName = conf["intermediateCaName"]
    else:
        intermediateCaName = caName

    subprocess.run(
        [
            "docker",
            "compose",
            "run",
            "--rm",
            "-v",
            f"{os.getcwd()}/data/volumes/{caName}/proxy-certs:/proxy:rw",
            "-v",
            f"{os.getcwd()}/data/secrets/{intermediateCaName}/provisioner-password:/provisioner-password:ro",
            f"{intermediateCaName}-ca",
            "step",
            "ca",
            "certificate",
            serverName,
            "/proxy/cert.crt",
            "/proxy/cert.key",
            "--provisioner=internal",
            "--password-file=/provisioner-password",
            "--set",
            f"crlDistributionPoints=http://{serverName}/crl",
            "--set",
            f"ocspServer=http://{serverName}/ocsp",
        ],
    )


def generateOCSPCert(mainConfig, caName, certName=None):
    print("Generating OCSP certificate")

    serverName = f"{caName}.{mainConfig['serverName']}"

    conf = readConfigFile(f"{DefaultFileLocations.configDir}/{caName}/config.json")
    if conf["type"] == "root-ca":
        intermediateCaName = conf["intermediateCaName"]
        certsPath = f"{DefaultFileLocations.volumesDir}/{caName}/ocsp-data"
    else:
        intermediateCaName = caName
        certsPath = f"{DefaultFileLocations.volumesDir}/{caName}/ocsp-certs"

        shutil.copy(
            f"data/configs/{caName}/ca/certs/intermediate_ca.crt",
            f"data/volumes/{caName}/ocsp-certs/ca.crt",
        )

    if certName is None:
        certName = f"{caName} OCSP"

    subprocess.run(
        [
            "docker",
            "compose",
            "run",
            "--rm",
            "-v",
            f"{os.getcwd()}/{certsPath}:/ocsp:rw",
            "-v",
            f"{os.getcwd()}/data/secrets/{intermediateCaName}/provisioner-password:/provisioner-password:ro",
            f"{intermediateCaName}-ca",
            "step",
            "ca",
            "certificate",
            certName,
            "/ocsp/ocsp.crt",
            "/ocsp/ocsp.key",
            "--provisioner=internal",
            "--password-file=/provisioner-password",
            "--set",
            f"crlDistributionPoints=http://{serverName}/crl",
            "--set",
            "isOCSP=true",
        ],
    )


def createProvisioner(mainConfig, caName):
    print("Creating internal provisioner")
    print(
        "When prompted for password, leave it empty, it will be generated automatically"
    )
    print("")

    passwordDir = DirOperations.createDir(DefaultFileLocations.secretsDir, caName)
    passwordFile = f"{passwordDir}/provisioner-password"

    subprocess.run(
        [
            "docker",
            "compose",
            "run",
            "--rm",
            "-v",
            f"{os.getcwd()}/static/stepca/templates/internal.tpl:/templates/internal.tpl:ro",
            f"{caName}-ca",
            "step",
            "ca",
            "provisioner",
            "add",
            "internal",
            "--type=JWK",
            "--create",
            "--x509-min-dur=24h",
            "--x509-default-dur=24h",
            "--x509-max-dur=24h",
            "--ssh=false",
            "--x509-template=/templates/internal.tpl",
            "--admin-name=step",
        ],
    )

    password = input("Add here the provisioner password: ")
    with open(passwordFile, "w") as f:
        f.write(password)
