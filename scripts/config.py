class Templates:
    templatesDir = "templates"
    dockerTemplatesDir = f"{templatesDir}/docker"
    proxyTemplatesDir = f"{templatesDir}/proxy"
    databaseTemplatesDir = f"{templatesDir}/database"
    caTemplatesDir = f"{templatesDir}/stepca"
    certRenewerTemplatesDir = f"{templatesDir}/cert-renewer"


class DefaultFileLocations:
    dockerComposeFile = "docker-compose.yml"

    dataDir = "data"

    ## Configs
    configDir = f"{dataDir}/configs"
    mainConfigFile = f"{dataDir}/config.json"

    ## Volumes
    volumesDir = f"{dataDir}/volumes"
    proxyCertsVolume = f"{volumesDir}/proxy-certs"
    databaseVolume = f"{volumesDir}/database"

    ## Secrets
    secretsDir = f"{dataDir}/secrets"
