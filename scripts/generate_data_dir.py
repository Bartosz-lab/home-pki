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

    shutil.copy(
        f"{Templates.templatesDir}/config.json.template",
        DefaultFileLocations.mainConfigFile,
    )

    # Create volumes directory
    os.makedirs(DefaultFileLocations.volumesDir)
    os.makedirs(DefaultFileLocations.proxyCertsVolume)
    os.makedirs(DefaultFileLocations.databaseVolume)
