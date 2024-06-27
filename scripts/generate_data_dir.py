import os
import shutil
import sys

from config import DefaultFileLocations, Templates


def main():
    print("Creating data directory.")
    if os.path.exists(DefaultFileLocations.dataDir):
        print("Data directory already exists.")
        sys.exit(1)

    os.makedirs(DefaultFileLocations.dataDir)
    os.makedirs(DefaultFileLocations.configDir)
    os.makedirs(DefaultFileLocations.secretsDir)

    shutil.copy(
        f"{Templates.templatesDir}/config.json.template",
        DefaultFileLocations.mainConfigFile,
    )
    shutil.copy(
        f"{Templates.templatesDir}/docker-compose.yml.template",
        DefaultFileLocations.dockerComposeFile,
    )

    with open(f"{DefaultFileLocations.secretsDir}/db-password.txt", "w") as f:
        f.write("<!!!!Ch@nge Me:( Please>")

    # Create volumes directory
    os.makedirs(DefaultFileLocations.volumesDir)
    os.makedirs(DefaultFileLocations.databaseVolume)
