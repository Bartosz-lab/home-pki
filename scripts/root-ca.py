import sys
import re

from helpers import readConfig, createDir, processTemplateAndSave, processTemplate
from config import Templates

if len(sys.argv) != 2:
    print("Usage: python scripts/root-ca.py <name>")
    sys.exit(1)

rootName = sys.argv[1]

# Check if the name is valid
if not re.match(r"^[a-z0-9\-]+$", rootName):
    print("Invalid name. Only small letters or '-' are allowed.")
    sys.exit(1)

resultDir = createDir(rootName)

proxyFile = f"{resultDir}/root-ca.conf"

# Read config from json file
config = readConfig()

# Generate docker include file
includeFile = f"{resultDir}/root-ca.yml"
processTemplateAndSave(
    f"{Templates.dockerTemplatesDir}/root-ca.yml.template",
    includeFile,
    {"rootName": rootName, "proxyFile": proxyFile},
)

# Generate proxy config
processTemplateAndSave(
    f"{Templates.proxyTemplatesDir}/root-ca.conf.template",
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
