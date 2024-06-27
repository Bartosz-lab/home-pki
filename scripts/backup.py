import os
import subprocess
import shutil


def main():
    backupDir = "backup"
    tmpDir = f"{backupDir}/tmp"
    archiveName = f"{backupDir}/backup-pki"

    if not os.path.exists(backupDir):
        os.makedirs(backupDir)

    if os.path.exists(tmpDir):
        shutil.rmtree(tmpDir)

    os.makedirs(tmpDir)

    shutil.copytree("data/configs", f"{tmpDir}/configs")
    shutil.copytree("data/secrets", f"{tmpDir}/secrets")
    shutil.copyfile("data/config.json", f"{tmpDir}/config.json")

    with open(f"{tmpDir}/database.sql", "w") as f:
        subprocess.run(
            [
                "docker",
                "compose",
                "exec",
                "database",
                "pg_dumpall",
                "-U",
                "postgres",
            ],
            stdout=f,
        )

    shutil.make_archive(archiveName, "gztar", tmpDir)

    shutil.rmtree(tmpDir)
