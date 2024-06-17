import os

__dir = "/usr/src/app/data"
indexFile = f"{__dir}/index.txt"
indexAttrFile = f"{__dir}/index.txt.attr"
totalCertsFile = f"{__dir}/total_certs.txt"
totalRevokedCertsFile = f"{__dir}/total_revoked_certs.txt"

# Number of minutes when fresh revocation information is available
nmin = str(os.getenv("OCSP_NMIN", 15))


class cronConfig:
    refreshFull = os.getenv("CRON_REFRESH_FULL", "0 0 * * *")
    refreshIncremental = os.getenv("CRON_REFRESH_INCREMENTAL", "*/15 * * * *")


class dbConfig:
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT", 5432)
    dbname = os.getenv("DB_NAME")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    limit = 1000
