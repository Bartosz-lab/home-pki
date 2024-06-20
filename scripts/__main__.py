import argparse
import os

from config import DefaultFileLocations
from helpers import readConfigFile

import initial
import root_ca
import intermediate_ca


parser = argparse.ArgumentParser(
    description="Program to generate config files.",
)
subparsers = parser.add_subparsers(
    dest="command", title="Commands", help="Commands help"
)

###########################
########## Common #########
###########################

config_parser = argparse.ArgumentParser(add_help=False)
config_parser.add_argument(
    "--config",
    action="store",
    default="configs-user/config.json",
    help=f'Location of the config file. Default: "{DefaultFileLocations.mainConfigFile}"',
    type=str,
)
update_parser = argparse.ArgumentParser(add_help=False)
update_parser.add_argument(
    "--update",
    action="store_true",
    help="Update the existing config files.Use when you change main config file or when updated repo to new version.",
)


###########################
########## Update #########
###########################
parser_initial = subparsers.add_parser(
    "update",
    help="Update all existing config files.",
    description="Update all existing config files.",
    parents=[config_parser],
)


###########################
######## Main init ########
###########################
parser_initial = subparsers.add_parser(
    "main-init",
    help="Create main config files.",
    description="Create main config files.",
    parents=[config_parser],
)


###########################
######### Root CA #########
###########################
parser_root_ca = subparsers.add_parser(
    "root-ca",
    help="Create root CA config files.",
    description="Create root CA config files.",
    parents=[config_parser, update_parser],
)
parser_root_ca.add_argument(
    "name",
    action="store",
    help="Name of the root CA.",
    type=str,
)


###########################
##### Intermediate CA #####
###########################
parser_intermediate_ca = subparsers.add_parser(
    "intermediate-ca",
    help="Create intermediate CA config files.",
    description="Create intermediate CA config files.",
    parents=[config_parser, update_parser],
)
parser_intermediate_ca.add_argument(
    "name",
    action="store",
    help="Name of the intermediate CA.",
    type=str,
)


###########################
########## Parse ##########
###########################

args = parser.parse_args()

if not args.command:
    parser.print_help()
    exit(1)

mainConfig = readConfigFile(args.config)

match args.command:
    case "update":
        initial.main(mainConfig)
        for dir in os.listdir(DefaultFileLocations.generatedConfigDir):
            if os.path.isdir(f"{DefaultFileLocations.generatedConfigDir}/{dir}"):
                conf = readConfigFile(
                    f"{DefaultFileLocations.generatedConfigDir}/{dir}/config.json"
                )
                if conf["type"] == "root-ca":
                    root_ca.main(mainConfig, dir, True)
                elif conf["type"] == "intermediate-ca":
                    intermediate_ca.main(mainConfig, dir, True)

    case "main-init":
        initial.main(mainConfig)
    case "root-ca":
        root_ca.main(mainConfig, args.name, args.update)
    case "intermediate-ca":
        intermediate_ca.main(mainConfig, args.name, args.update)
    case _:
        parser.print_help()
