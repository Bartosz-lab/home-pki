import json
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
proxyFile = f"{resultDir}/intermediate-ca.conf"
includeFile = f"{resultDir}/intermediate-ca.yml"

# Read the main config
mainConfig = readMainConfig()

# Generate docker include file
processTemplateAndSave(
    f"{Templates.dockerTemplatesDir}/intermediate-ca.yml.template",
    includeFile,
    {
        "caName": caName,
        "proxyFile": proxyFile,
        "databaseFile": databaseFile,
        "dbPassword": dbPassword,
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
    f"{Templates.proxyTemplatesDir}/intermediate-ca.conf.template",
    proxyFile,
    {"caName": caName, "serverName": f"{caName}.{mainConfig["domain"]}"},
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
