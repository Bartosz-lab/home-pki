from helpers import (
    DirOperations,
    validateName,
    readConfigFile,
    processTemplateAndSave,
    processTemplate,
    generatePassword,
    saveConfig,
)
from config import Templates, DefaultFileLocations


def main(mainConfig, caName, update=False, rootFingerprint=None):
    validateName(caName)

    if update:
        print(f"{caName}: Updating intermediate CA config files.")
        configDir = DirOperations.createDirIfNotExists(
            DefaultFileLocations.configDir, caName
        )

        conf = readConfigFile(f"{configDir}/config.json")
        dbPassword = conf["dbPassword"]
        if not rootFingerprint:
            rootFingerprint = conf["rootFingerprint"]
    else:
        print(f"{caName}: Creating intermediate CA config files.")
        if not rootFingerprint:
            print("Please provide the fingerprint of the root CA.")
            exit(1)
        configDir = DirOperations.createDir(DefaultFileLocations.configDir, caName)

        dbPassword = generatePassword()

    serverName = f"{caName}.{mainConfig['serverName']}"

    # Generate config directories
    caConfigDir = DirOperations.createDirIfNotExists(configDir, "ca")
    caStepcaConfigDir = DirOperations.createDirIfNotExists(caConfigDir, "config")
    caCertsDir = DirOperations.createDirIfNotExists(caConfigDir, "certs")
    DirOperations.createDirIfNotExists(caConfigDir, "secrets")

    # Generate volume directories
    volumesDir = DirOperations.createDirIfNotExists(
        DefaultFileLocations.volumesDir, caName
    )
    ocspCertsVolume = DirOperations.createDirIfNotExists(volumesDir, "ocsp-certs")
    proxyCertsVolume = DirOperations.createDirIfNotExists(volumesDir, "proxy-certs")

    # Generate database setup file
    databaseFile = f"{configDir}/init-database.sh"
    databaseTemplate = f"{Templates.databaseTemplatesDir}/init-database.sh.template"
    processTemplateAndSave(
        databaseTemplate,
        databaseFile,
        {"dbUser": caName, "dbPassword": dbPassword},
    )

    # Generate proxy config
    proxyFile = f"{configDir}/intermediate-ca.conf"
    proxyTemplate = f"{Templates.proxyTemplatesDir}/intermediate-ca.conf.template"
    processTemplateAndSave(
        proxyTemplate,
        proxyFile,
        {"caName": caName, "serverName": serverName},
    )

    # Generate CA config
    caConfigFile = f"{caStepcaConfigDir}/ca.json"
    caConfigTemplate = f"{Templates.caTemplatesDir}/ca.json.template"
    processTemplateAndSave(
        caConfigTemplate,
        caConfigFile,
        {"caName": caName, "serverName": serverName},
    )

    caDefaultsFile = f"{caStepcaConfigDir}/defaults.json"
    caDefaultsTemplate = f"{Templates.caTemplatesDir}/defaults.json.template"
    processTemplateAndSave(
        caDefaultsTemplate,
        caDefaultsFile,
        {"caName": caName, "fingerprint": rootFingerprint},
    )

    # Generate refresh certs script
    renewCertsFile = f"{configDir}/cert-renew.sh"
    renewCertsTemplate = f"{Templates.certRenewerTemplatesDir}/cert-renew.sh.template"
    processTemplateAndSave(
        renewCertsTemplate,
        renewCertsFile,
        {
            "caName": caName,
            "proxyCertsVolume": proxyCertsVolume,
        },
    )

    # Generate docker include file
    includeFile = f"{configDir}/intermediate-ca.yml"
    includeTemplate = f"{Templates.dockerTemplatesDir}/intermediate-ca.yml.template"
    processTemplateAndSave(
        includeTemplate,
        includeFile,
        {
            "caName": caName,
            "proxyFile": proxyFile,
            "databaseFile": databaseFile,
            "dbPassword": dbPassword,
            "caConfigDir": caConfigDir,
            "ocspCertsVolume": ocspCertsVolume,
            "proxyCertsVolume": proxyCertsVolume,
            "renewCertsFile": renewCertsFile,
            "rootCaFile": f"{caCertsDir}/root_ca.crt",
        },
    )

    # Print config to attach to the main docker-compose file
    if not update:
        print("Add the following lines to the main docker-compose.yml file:")
        print(
            processTemplate(
                f"{Templates.dockerTemplatesDir}/intermediate-ca-include.template",
                {"includeFile": includeFile, "caName": caName},
            )
        )

    # Save the new config
    saveConfig(
        {
            "caName": caName,
            "type": "intermediate-ca",
            "dbPassword": dbPassword,
            "rootFingerprint": rootFingerprint,
        },
        configDir,
    )
