import os
import re
import sys
import json
import secrets
import string
from typing import Mapping

from config import configDir


def validateName(name: str) -> None:
    """Check if the name is valid."""
    if not re.match(r"^[a-z0-9\-]+$", name):
        print("Invalid name. Only small letters or '-' are allowed.")
        sys.exit(1)


def readMainConfig() -> Mapping[str, object]:
    """Read the configuration file."""
    return readConfigFile(f"{configDir}/config.json")


def readConfigFile(file: str) -> Mapping[str, object]:
    """Read the configuration file."""
    if not os.path.exists(file):
        print(f"{file} file does not exist.")
        sys.exit(1)

    with open(file) as f:
        config = json.load(f)

    return config


def createDir(name: str) -> str:
    """
    Create a directory in configDir. Exit program if the directory already exists.
    Return the directory path.
    """
    dir = f"{configDir}/{name}"
    if os.path.exists(dir):
        print("Result directory already exists.")
        sys.exit(1)

    os.makedirs(dir)
    return dir


def processTemplateAndSave(
    src: str, dest: str, params: Mapping[str, object] = {}
) -> None:
    """Generate a file from a template file."""
    result = processTemplate(src, params)
    with open(dest, "w") as f:
        f.write(result)


def processTemplate(src: str, params: Mapping[str, object] = {}) -> str:
    """Generate a string from a template file."""
    with open(src, "r") as f:
        src = string.Template(f.read())

    return src.substitute(params)


def generatePassword() -> str:
    """Generate a random password."""
    alphabet = string.ascii_letters + string.digits + "!@#%^&*()_+{}:<>?"
    return "".join(secrets.choice(alphabet) for _ in range(40))


def saveConfig(config: Mapping[str, object], dir: str) -> None:
    """Save the configuration file."""
    with open(f"{dir}/config.json", "w") as f:
        json.dump(config, f, indent=4)
