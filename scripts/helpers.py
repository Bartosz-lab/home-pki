import os
import sys
import json
from string import Template
from typing import Mapping

from config import configDir


def readConfig() -> Mapping[str, object]:
    """Read the configuration file."""
    config_file = f"{configDir}/config.json"
    if not os.path.exists(config_file):
        print("config.json file does not exist. Read the README.md file.")
        sys.exit(1)

    with open(config_file) as f:
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
        src = Template(f.read())

    return src.substitute(params)
