import os
import sys
import subprocess

from config import (
    indexFile,
    indexAttrFile,
    totalCertsFile,
    totalRevokedCertsFile,
    nmin,
    cronConfig,
)
from periodic_check import periodicCheck


def main():
    print("Init container started")

    if not os.path.isfile(indexFile):
        with open(indexFile, "w") as f:
            f.write("")
            print("indexFile created with 0 certs")

    if not os.path.isfile(indexAttrFile):
        with open(indexAttrFile, "w") as f:
            f.write("unique_subject=no")
            print("indexAtrFile created with 0 certs")

    if not os.path.isfile(totalCertsFile):
        with open(totalCertsFile, "w") as f:
            f.write("0")
            print("totalCertsFile created with 0 certs")

    if not os.path.isfile(totalRevokedCertsFile):
        with open(totalRevokedCertsFile, "w") as f:
            f.write("0")
            print("totalRevokedCertsFile created with 0 certs")

    with open("/etc/crontabs/root", "w") as f:
        f.write(
            f"{cronConfig.refreshFull} /usr/local/bin/python /usr/src/app/refresher.py\n"
        )
        f.write(
            f"{cronConfig.refreshIncremental} /usr/local/bin/python /usr/src/app/periodic_check.py\n"
        )

    print("Starting periodic check")
    periodicCheck()

    print("Starting OCSP responder")
    sys.stdout.flush()
    subprocess.Popen(
        [
            "inotifyd",
            "reboot",
            "/usr/src/app/certs/ocsp.crt:c",
        ]
    )
    subprocess.Popen(
        [
            "openssl",
            "ocsp",
            "-index",
            "/usr/src/app/data/index.txt",
            "-port",
            "80",
            "-rsigner",
            "/usr/src/app/certs/ocsp.crt",
            "-rkey",
            "/usr/src/app/certs/ocsp.key",
            "-CA",
            "/usr/src/app/certs/ca.crt",
            "-nmin",
            nmin,
            "-multi",
            "4",
            "-timeout",
            "600",  # 10 minutes
            "-ignore_err",
        ]
    )
    os.execve("/usr/sbin/crond", ["crond", "-f"], os.environ)


if __name__ == "__main__":
    main()
