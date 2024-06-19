import os
import sys

from helpers import (
    validateName,
    readMainConfig,
    readConfigFile,
    createDir,
    processTemplateAndSave,
    processTemplate,
    generatePassword,
    saveConfig,
)
from config import Templates

if len(sys.argv) != 2:
    print("Usage: python scripts/intermediate-ca.py <name>")
    sys.exit(1)

caName = sys.argv[1]
validateName(caName)

resultDir = createDir(caName)

## Gnerate config variables
if os.path.isfile(f"{resultDir}/config.json"):
    conf = readConfigFile(f"{resultDir}/config.json")
    caName = conf["caName"]
    # TODO: Replace this with file secret
    dbPassword = conf["dbPassword"]
else:
    dbPassword = generatePassword()

databaseFile = f"{resultDir}/init-database.sh"
proxyFile = f"{resultDir}/intermediate-ca.http"
proxyHttpsFile = f"{resultDir}/intermediate-ca.https"
includeFile = f"{resultDir}/intermediate-ca.yml"
caConfigDir = f"{resultDir}/config"

# Read the main config
mainConfig = readMainConfig()

# Generate docker include file
processTemplateAndSave(
    f"{Templates.dockerTemplatesDir}/intermediate-ca.yml.template",
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

# Generate database setup file
processTemplateAndSave(
    f"{Templates.databaseTemplatesDir}/init-database.sh.template",
    databaseFile,
    {"dbUser": caName, "dbPassword": dbPassword},
)

# Generate proxy config
processTemplateAndSave(
    f"{Templates.proxyTemplatesDir}/intermediate-ca.http.template",
    proxyFile,
    {"caName": caName},
)
processTemplateAndSave(
    f"{Templates.proxyTemplatesDir}/intermediate-ca.https.template",
    proxyHttpsFile,
    {"caName": caName},
)

# Generate CA config
os.makedirs(caConfigDir)

processTemplateAndSave(
    f"{Templates.caTemplatesDir}/ca.json.template",
    f"{caConfigDir}/ca.json",
    {"serverName": mainConfig["serverName"]},
)
processTemplateAndSave(
    f"{Templates.caTemplatesDir}/defaults.json.template",
    f"{caConfigDir}/defaults.json",
    {},
)

# Print config to attach to the main docker-compose file
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
        "dbPassword": dbPassword,
    },
    resultDir,
)
