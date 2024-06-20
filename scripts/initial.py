from helpers import (
    processTemplateAndSave,
)
from config import DefaultFileLocations, Templates


def main(mainConfig):
    print("Creating main config files.")

    serverName = mainConfig["serverName"]
    proxyTemplate = f"{Templates.proxyTemplatesDir}/proxy.conf.template"
    proxyFile = f"{DefaultFileLocations.configDir}/proxy.conf"

    # Generate main proxy config
    processTemplateAndSave(
        proxyTemplate,
        proxyFile,
        {"serverName": serverName},
    )
