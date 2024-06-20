class Templates:
    templatesDir = "templates"
    dockerTemplatesDir = f"{templatesDir}/docker"
    proxyTemplatesDir = f"{templatesDir}/proxy"
    databaseTemplatesDir = f"{templatesDir}/database"
    caTemplatesDir = f"{templatesDir}/stepca"


class DefaultFileLocations:
    generatedConfigDir = "configs"
    userProvidedConfigDir = "configs-user"

    mainConfigFile = f"{userProvidedConfigDir}/config.json"
