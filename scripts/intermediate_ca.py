from helpers import (
    DirOperations,
    validateName,
    readConfigFile,
    processTemplateAndSave,
    processTemplate,
    generatePassword,
    saveConfig,
)
from config import Templates


def main(mainConfig, caName, update=False):
    validateName(caName)

    if update:
        print(f"{caName}: Updating intermediate CA config files.")
        resultDir = DirOperations.createDirIfNotExists(caName)

        conf = readConfigFile(f"{resultDir}/config.json")
        dbPassword = conf["dbPassword"]
    else:
        print(f"{caName}: Creating intermediate CA config files.")
        resultDir = DirOperations.createDir(caName)
        dbPassword = generatePassword()

    # Generate database setup file
    databaseFile = f"{resultDir}/init-database.sh"
    databaseTemplate = f"{Templates.databaseTemplatesDir}/init-database.sh.template"
    processTemplateAndSave(
        databaseTemplate,
        databaseFile,
        {"dbUser": caName, "dbPassword": dbPassword},
    )

    # Generate proxy config
    proxyFile = f"{resultDir}/intermediate-ca.http"
    proxyTemplate = f"{Templates.proxyTemplatesDir}/intermediate-ca.http.template"
    processTemplateAndSave(
        proxyTemplate,
        proxyFile,
        {"caName": caName},
    )

    proxyHttpsFile = f"{resultDir}/intermediate-ca.https"
    proxyHttpsTemplate = f"{Templates.proxyTemplatesDir}/intermediate-ca.https.template"
    processTemplateAndSave(
        proxyHttpsTemplate,
        proxyHttpsFile,
        {"caName": caName},
    )

    # Generate CA config
    caConfigDir = DirOperations.createDirIfNotExistsInDir(resultDir, "ca")

    caConfigFile = f"{caConfigDir}/ca.json"
    caConfigTemplate = f"{Templates.caTemplatesDir}/ca.json.template"
    processTemplateAndSave(
        caConfigTemplate,
        caConfigFile,
        {"serverName": mainConfig["serverName"]},
    )

    caDefaultsFile = f"{caConfigDir}/defaults.json"
    caDefaultsTemplate = f"{Templates.caTemplatesDir}/defaults.json.template"
    processTemplateAndSave(
        caDefaultsTemplate,
        caDefaultsFile,
        {},
    )

    # Generate docker include file
    includeFile = f"{resultDir}/intermediate-ca.yml"
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
        resultDir,
    )
