import os
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
from config import configDir, Templates

# Read the main config
mainConfig = readMainConfig()
serverName = mainConfig["serverName"]

proxyFile = f"{configDir}/proxy.conf"

# Generate main proxy config
processTemplateAndSave(
    f"{Templates.proxyTemplatesDir}/proxy.conf.template",
    proxyFile,
    {"serverName": serverName},
)
