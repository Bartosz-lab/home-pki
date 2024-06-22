import argparse
import os

from config import DefaultFileLocations
from helpers import readConfigFile

import generate_data_dir
import root_ca
import intermediate_ca
import generate_certs


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
    default=DefaultFileLocations.mainConfigFile,
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
#### Generate Data Dir ####
###########################
parser_generate_data_dir = subparsers.add_parser(
    "generate-data-dir",
    help="Generate data directory.",
    description="Generate data directory.",
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
parser_root_ca.add_argument(
    "--intCa",
    action="store",
    help="Name of the intermediate CA for generating OCSP and proxy certs. Required if --update is not provided.",
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
parser_intermediate_ca.add_argument(
    "--fingerprint",
    action="store",
    help="Fingerprint of the root CA. Required if --update is not provided.",
    type=str,
)


###########################
### Generate Proxy Certs ##
###########################

parser_generate_proxy_certs = subparsers.add_parser(
    "generate-proxy-certs",
    help="Generate proxy certificates.",
    description="Generate proxy certificates.",
    parents=[config_parser],
)
parser_generate_proxy_certs.add_argument(
    "name",
    action="store",
    help="Name of the CA.",
    type=str,
)
parser_generate_proxy_certs.add_argument(
    "--intCa",
    action="store",
    help="Name of the intermediate CA for generating OCSP and proxy certs. If not provided, it will be same as CA name.",
    type=str,
)

###########################
### Generate OCSP Certs ###
###########################

parser_generate_ocsp_certs = subparsers.add_parser(
    "generate-ocsp-certs",
    help="Generate OCSP certificates for Intermediate CA.",
    description="Generate OCSP certificates for Intermediate CA.",
    parents=[config_parser],
)
parser_generate_ocsp_certs.add_argument(
    "name",
    action="store",
    help="Name of the CA.",
    type=str,
)
parser_generate_ocsp_certs.add_argument(
    "--certName",
    action="store",
    help='Name of the certificate. if not provided, it will be "<name> OCSP".',
    type=str,
)
parser_generate_ocsp_certs.add_argument(
    "--intCa",
    action="store",
    help="Name of the intermediate CA for generating OCSP and proxy certs. If not provided, it will be same as CA name.",
    type=str,
)


###########################
########## Parse ##########
###########################

args = parser.parse_args()

if not args.command:
    parser.print_help()
    exit(1)


match args.command:
    case "generate-data-dir":
        generate_data_dir.main()
    case "update":
        mainConfig = readConfigFile(args.config)
        for dir in os.listdir(DefaultFileLocations.configDir):
            if os.path.isdir(f"{DefaultFileLocations.configDir}/{dir}"):
                conf = readConfigFile(
                    f"{DefaultFileLocations.configDir}/{dir}/config.json"
                )
                if conf["type"] == "root-ca":
                    root_ca.main(mainConfig, dir, True)
                elif conf["type"] == "intermediate-ca":
                    intermediate_ca.main(mainConfig, dir, True)

    case "root-ca":
        root_ca.main(readConfigFile(args.config), args.name, args.update, args.intCa)
    case "intermediate-ca":
        intermediate_ca.main(
            readConfigFile(args.config), args.name, args.update, args.fingerprint
        )
    case "generate-proxy-certs":
        generate_certs.generateProxyCert(
            readConfigFile(args.config), args.name, args.intCa
        )
    case "generate-ocsp-certs":
        if args.intCa is None:

            generate_certs.generateOCSPCert(
                readConfigFile(args.config), args.name, args.certName
            )
        else:
            generate_certs.generateOCSPCertForRootCA(
                readConfigFile(args.config), args.name, args.intCa, args.certName
            )
    case _:
        parser.print_help()
