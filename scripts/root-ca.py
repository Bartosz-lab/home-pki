import os
import sys

from helpers import saveConfig, validateName, readMainConfig, readConfigFile, createDir, processTemplateAndSave, processTemplate
from config import Templates

if len(sys.argv) != 2:
    print("Usage: python scripts/root-ca.py <name>")
    sys.exit(1)

rootName = sys.argv[1]
validateName(rootName)

resultDir = createDir(rootName)

## Gnerate config variables
if os.path.isfile(f"{resultDir}/config.json"):
    conf = readConfigFile(f"{resultDir}/config.json")
    rootName = conf["rootName"]


proxyFile = f"{resultDir}/root-ca.http"

# Read config from json file
config = readMainConfig()

# Generate docker include file
includeFile = f"{resultDir}/root-ca.yml"
processTemplateAndSave(
    f"{Templates.dockerTemplatesDir}/root-ca.yml.template",
    includeFile,
    {"rootName": rootName, "proxyFile": proxyFile},
)

# Generate proxy config
processTemplateAndSave(
    f"{Templates.proxyTemplatesDir}/root-ca.http.template",
    proxyFile,
    {"rootName": rootName, "serverName": f"{rootName}.{config["domain"]}"},
)

# Print config to attach to the main docker-compose file
print("Add the following lines to the main docker-compose.yml file:")
print(
    processTemplate(
        f"{Templates.dockerTemplatesDir}/root-ca-include.template",
        {"includeFile": includeFile, "rootName": rootName},
    )
)

# Save the new config
saveConfig(
    {
        "rootName": rootName,
    },
    resultDir,
)
