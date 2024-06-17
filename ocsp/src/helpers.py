from datetime import datetime, timezone
from typing import Any, Dict

from psycopg import Cursor, ServerCursor

from config import totalCertsFile, totalRevokedCertsFile, indexFile


class DateHelper:
    """Helper class for date operations."""

    @staticmethod
    def convertDateToOpensslFormat(date: datetime) -> str:
        # Convert date to OpenSSL format
        return date.strftime("%y%m%d%H%M%SZ")

    @staticmethod
    def convertIsoToOpensslFormat(date_str: str) -> str:
        # Convert ISO 8601 to OpenSSL format
        dt = datetime.fromisoformat(date_str)
        return DateHelper.convertDateToOpensslFormat(dt)

    @staticmethod
    def nowOpensslFormat() -> str:
        # Get current time in OpenSSL format
        return DateHelper.convertDateToOpensslFormat(datetime.now(timezone.utc))


class DataHelper:
    """Helper class for data operations."""

    @staticmethod
    def getTotalCerts() -> int:
        """Get total number of certificates checked last time."""
        with open(totalCertsFile, "r") as f:
            return int(f.read())

    @staticmethod
    def setTotalCerts(totalCerts: int) -> None:
        """Set total number of checked certificates."""
        with open(totalCertsFile, "w") as f:
            f.write(str(totalCerts))

    @staticmethod
    def getTotalRevokedCerts() -> int:
        """Get total number of revoked certificates checked last time."""
        with open(totalRevokedCertsFile, "r") as f:
            return int(f.read())

    @staticmethod
    def setTotalRevokedCerts(totalRevokedCerts: int) -> None:
        """Set total number of revoked checked certificates."""
        with open(totalRevokedCertsFile, "w") as f:
            f.write(str(totalRevokedCerts))

    @staticmethod
    def getIndexData() -> Dict[int, str]:
        """Get data from index file."""
        result = {}
        with open(indexFile, "r") as f:
            for line in f:
                serial = line.split("\t")[3]
                result[serial] = line
        return result

    @staticmethod
    def setIndexData(data: Dict[int, str]) -> None:
        """Set data to index file."""
        with open(indexFile, "w") as f:
            f.write("".join(data.values()))

    @staticmethod
    def formatIndexData(
        status: str,
        notAfter: str,
        serial: str,
        revokedAt: str = "",
    ) -> str:
        """Format data for index file."""
        return f"{status}\t{notAfter}\t{revokedAt}\t{serial}\tunknown\tdummy\n"


class DatabaseHelper:
    """Helper class for database operations."""

    @staticmethod
    def getTotalCerts(cursor: Cursor[Any] | ServerCursor[Any]) -> int:
        """Get total number of certificates in the database."""
        cursor.execute("select count(*) from x509_certs")
        return cursor.fetchone()[0]

    @staticmethod
    def getTotalRevokedCerts(cursor: Cursor[Any] | ServerCursor[Any]) -> int:
        """Get total number of revoked certificates in the database."""
        cursor.execute("select count(*) from revoked_x509_certs")
        return cursor.fetchone()[0]
