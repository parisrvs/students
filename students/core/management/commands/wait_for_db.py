"""
Django command to wait for the database to be available
"""

from django.core.management.base import BaseCommand
from django.db.utils import OperationalError
from mysql.connector.errors import OperationalError as MySqlError
import time


class Command(BaseCommand):
    """Django command to wait for the database"""

    def handle(self, *args, **options):
        """Entrypoint for command"""
        self.stdout.write("Waiting for database...")
        db_up = False
        while db_up is False:
            try:
                self.check(databases=["default"])
                db_up = True
            except (MySqlError, OperationalError):
                self.stdout.write(
                    "Database unavailable, waiting for 1 seconds...")
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS("Database available!"))
