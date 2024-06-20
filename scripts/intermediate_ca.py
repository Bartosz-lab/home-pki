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


def main(mainConfig, caName, update=False):
    validateName(caName)

    if update:
        print(f"{caName}: Updating intermediate CA config files.")
        configDir = DirOperations.createDirIfNotExists(
            DefaultFileLocations.configDir, caName
        )

        conf = readConfigFile(f"{configDir}/config.json")
        dbPassword = conf["dbPassword"]
    else:
        print(f"{caName}: Creating intermediate CA config files.")
        configDir = DirOperations.createDir(DefaultFileLocations.configDir, caName)

        dbPassword = generatePassword()

    # Generate config directories
    caConfigDir = DirOperations.createDirIfNotExists(configDir, "ca")
    caStepcaConfigDir = DirOperations.createDirIfNotExists(caConfigDir, "config")
    DirOperations.createDirIfNotExists(caConfigDir, "secrets")
    DirOperations.createDirIfNotExists(caConfigDir, "certs")

    # Generate volume directories
    volumesDir = DirOperations.createDirIfNotExists(
        DefaultFileLocations.volumesDir, caName
    )
    ocspCertsVolume = DirOperations.createDirIfNotExists(volumesDir, "ocsp-certs")

    # Generate database setup file
    databaseFile = f"{configDir}/init-database.sh"
    databaseTemplate = f"{Templates.databaseTemplatesDir}/init-database.sh.template"
    processTemplateAndSave(
        databaseTemplate,
        databaseFile,
        {"dbUser": caName, "dbPassword": dbPassword},
    )

    # Generate proxy config
    proxyFile = f"{configDir}/intermediate-ca.http"
    proxyTemplate = f"{Templates.proxyTemplatesDir}/intermediate-ca.http.template"
    processTemplateAndSave(
        proxyTemplate,
        proxyFile,
        {"caName": caName},
    )

    proxyHttpsFile = f"{configDir}/intermediate-ca.https"
    proxyHttpsTemplate = f"{Templates.proxyTemplatesDir}/intermediate-ca.https.template"
    processTemplateAndSave(
        proxyHttpsTemplate,
        proxyHttpsFile,
        {"caName": caName},
    )

    # Generate CA config
    caConfigFile = f"{caStepcaConfigDir}/ca.json"
    caConfigTemplate = f"{Templates.caTemplatesDir}/ca.json.template"
    processTemplateAndSave(
        caConfigTemplate,
        caConfigFile,
        {"caName": caName, "serverName": mainConfig["serverName"]},
    )

    caDefaultsFile = f"{caStepcaConfigDir}/defaults.json"
    caDefaultsTemplate = f"{Templates.caTemplatesDir}/defaults.json.template"
    processTemplateAndSave(
        caDefaultsTemplate,
        caDefaultsFile,
        {"caName": caName, "fingerprint": "Unimplemented"},
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
            "proxyHttpsFile": proxyHttpsFile,
            "databaseFile": databaseFile,
            "dbPassword": dbPassword,
            "caConfigDir": caConfigDir,
            "ocspCertsVolume": ocspCertsVolume,
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
        },
        configDir,
    )
