import json
import psycopg
from typing import Any, Dict
from OpenSSL import crypto
from psycopg import Cursor
from psycopg import ServerCursor

from helpers import (
    DateHelper,
    DataHelper,
    DatabaseHelper,
)
from config import dbConfig


def __getCerts(
    resultMap: Dict[int, str],
    cursor: Cursor[Any] | ServerCursor[Any],
    full: bool = False,
):
    """Get certificates from the database."""
    nowDate = DateHelper.nowOpensslFormat()
    offset = 0 if full else int(DataHelper.getTotalCerts())
    total = DatabaseHelper.getTotalCerts(cursor)
    DataHelper.setTotalCerts(total)

    while offset < total:
        cursor.execute(
            "select nvalue from x509_certs offset %s limit %s",
            (offset, dbConfig.limit),
        )
        offset += dbConfig.limit

        for (data,) in cursor.fetchall():
            cert = crypto.load_certificate(crypto.FILETYPE_ASN1, data)

            # Year should be 2 digits
            notAfter = cert.get_notAfter().decode("utf-8")[2:]
            serial = format(cert.get_serial_number(), "X")
            status = "V" if notAfter > nowDate else "E"

            resultMap[serial] = DataHelper.formatIndexData(
                status=status, notAfter=notAfter, serial=serial
            )


def __getCevoked(
    resultMap: Dict[int, str],
    cursor: Cursor[Any] | ServerCursor[Any],
    full: bool = False,
):
    """Get revoked certificates from the database."""
    offset = 0 if full else int(DataHelper.getTotalRevokedCerts())
    total = DatabaseHelper.getTotalRevokedCerts(cursor)
    DataHelper.setTotalRevokedCerts(total)

    while offset < total:
        cursor.execute(
            "select nvalue from revoked_x509_certs offset %s limit %s",
            (offset, dbConfig.limit),
        )
        offset += dbConfig.limit

        for (data,) in cursor.fetchall():
            parsed = json.loads(data)

            serial = format(int(parsed["Serial"]), "X")
            notAfter = DateHelper.convertIsoToOpensslFormat(parsed["ExpiresAt"])
            revokedAt = DateHelper.convertIsoToOpensslFormat(parsed["RevokedAt"])

            resultMap[serial] = DataHelper.formatIndexData(
                status="R",
                notAfter=notAfter,
                revokedAt=revokedAt,
                serial=serial,
            )


def refresh(
    full: bool = False,
):
    """
    Refresh the index file. If full is True, refresh all data, otherwise only new data.

    This function assumes that the records in the database respond with the added order.
    And also that records in the database are never deleted.
    """
    resultMap = {}

    if not full:
        resultMap = DataHelper.getIndexData()

    with psycopg.connect(
        host=dbConfig.host,
        port=dbConfig.port,
        dbname=dbConfig.dbname,
        user=dbConfig.user,
        password=dbConfig.password,
    ) as conn:
        print("Connected to the PostgreSQL server. - Refresher")

        with conn.cursor() as cursor:
            __getCerts(resultMap, cursor, full)
            __getCevoked(resultMap, cursor, full)

    DataHelper.setIndexData(resultMap)


if __name__ == "__main__":
    refresh(True)
