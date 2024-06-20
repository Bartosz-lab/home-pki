from helpers import (
    DirOperations,
    saveConfig,
    validateName,
    readConfigFile,
    processTemplateAndSave,
    processTemplate,
)
from config import Templates


def main(mainConfig, caName, update=False):
    validateName(caName)

    if update:
        print(f"{caName}: Updating root CA config files.")
        resultDir = DirOperations.createDirIfNotExists(caName)

        conf = readConfigFile(f"{resultDir}/config.json")
    else:
        print(f"{caName}: Creating root CA config files.")
        resultDir = DirOperations.createDir(caName)

    # Generate proxy config
    proxyFile = f"{resultDir}/root-ca.http"
    proxyTemplate = f"{Templates.proxyTemplatesDir}/root-ca.http.template"
    processTemplateAndSave(
        proxyTemplate,
        proxyFile,
        {
            "caName": caName,
        },
    )

    # Generate docker include file
    includeFile = f"{resultDir}/root-ca.yml"
    includeTemplate = f"{Templates.dockerTemplatesDir}/root-ca.yml.template"
    processTemplateAndSave(
        includeTemplate,
        includeFile,
        {"caName": caName, "proxyFile": proxyFile},
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
        },
        resultDir,
    )
