from helpers import (
    DirOperations,
    saveConfig,
    validateName,
    readConfigFile,
    processTemplateAndSave,
    processTemplate,
)
from config import Templates, DefaultFileLocations


def main(mainConfig, caName, update=False, intermediateCaName=None):
    validateName(caName)

    if update:
        print(f"{caName}: Updating root CA config files.")
        configDir = DirOperations.createDirIfNotExists(
            DefaultFileLocations.configDir, caName
        )

        conf = readConfigFile(f"{configDir}/config.json")
        if not intermediateCaName:
            intermediateCaName = conf["intermediateCaName"]

    else:
        print(f"{caName}: Creating root CA config files.")
        configDir = DirOperations.createDir(DefaultFileLocations.configDir, caName)
        if not intermediateCaName:
            print("Please provide the name of the intermediate CA.")
            exit(1)

    serverName = f"{caName}.{mainConfig['serverName']}"

    # Generate volume directories
    volumesDir = DirOperations.createDirIfNotExists(
        DefaultFileLocations.volumesDir, caName
    )
    ocspDataVolume = DirOperations.createDirIfNotExists(volumesDir, "ocsp-data")
    proxyCertsVolume = DirOperations.createDirIfNotExists(volumesDir, "proxy-certs")

    # Generate proxy config
    proxyFile = f"{configDir}/root-ca.conf"
    proxyTemplate = f"{Templates.proxyTemplatesDir}/root-ca.conf.template"
    processTemplateAndSave(
        proxyTemplate,
        proxyFile,
        {"caName": caName, "serverName": serverName},
    )

    # Generate refresh certs script
    renewCertsFile = f"{configDir}/cert-renew.sh"
    renewCertsTemplate = f"{Templates.certRenewerTemplatesDir}/cert-renew.sh.template"
    processTemplateAndSave(
        renewCertsTemplate,
        renewCertsFile,
        {
            "caName": caName,
            "intermediateCaName": intermediateCaName,
        },
    )

    # Generate docker include file
    includeFile = f"{configDir}/root-ca.yml"
    includeTemplate = f"{Templates.dockerTemplatesDir}/root-ca.yml.template"
    processTemplateAndSave(
        includeTemplate,
        includeFile,
        {
            "caName": caName,
            "proxyFile": proxyFile,
            "renewCertsFile": renewCertsFile,
            "ocspDataVolume": ocspDataVolume,
            "proxyCertsVolume": proxyCertsVolume,
            "rootCaFile": f"{ocspDataVolume}/ca.crt",
            "intermediateCaName": intermediateCaName,
            "crlFile": f"{configDir}/crl.pem",
        },
    )

    # Print config to attach to the main docker-compose file
    if not update:
        print("Add the following lines to the main docker-compose.yml file:")
        print(
            processTemplate(
                f"{Templates.dockerTemplatesDir}/root-ca-include.template",
                {"includeFile": includeFile, "caName": caName},
            )
        )

    # Save the new config
    saveConfig(
        {
            "caName": caName,
            "type": "root-ca",
            "intermediateCaName": intermediateCaName,
        },
        configDir,
    )
