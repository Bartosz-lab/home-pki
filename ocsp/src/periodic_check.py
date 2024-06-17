import psycopg

from config import dbConfig
from helpers import DataHelper
from refresher import refresh


def periodicCheck():
    callRefresher = False

    with psycopg.connect(
        host=dbConfig.host,
        port=dbConfig.port,
        dbname=dbConfig.dbname,
        user=dbConfig.user,
        password=dbConfig.password,
    ) as conn:
        print("Connected to the PostgreSQL server. - Periodic Check")

        with conn.cursor() as cur:
            cur.execute("select count(*) from x509_certs")
            totalCerts = str(cur.fetchone()[0])

            oldTotalCerts = DataHelper.getTotalCerts()
            if oldTotalCerts != totalCerts:
                callRefresher = True

            cur.execute("select * from revoked_x509_certs")
            totalRevokedCerts = str(cur.fetchone()[0])

            oldTotalRevokedCerts = DataHelper.getTotalRevokedCerts()
            if oldTotalRevokedCerts != totalRevokedCerts:
                callRefresher = True

    if callRefresher:
        refresh()


if __name__ == "__main__":
    periodicCheck()
