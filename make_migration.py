import argparse
import getpass
import hashlib
import re
from datetime import datetime
from pathlib import Path
from typing import List
from uuid import uuid4

CHANGELOG_XML_TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
<databaseChangeLog xmlns="http://www.liquibase.org/xml/ns/dbchangelog"
                   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                   xsi:schemaLocation="http://www.liquibase.org/xml/ns/dbchangelog
                   http://www.liquibase.org/xml/ns/dbchangelog/dbchangelog-3.1.xsd">
                   {}
</databaseChangeLog>
"""

MIGRATION_TEMPLATE = '<include file="{filename}" relativeToChangelogFile="true" />'


class MakeMigration:
    def __init__(self, migrations_path: str, message: str):
        self.migrations_path = migrations_path
        self.migrate_location: Path = Path(migrations_path)
        self.message = message

    @staticmethod
    def generate_liquibase_info_string(version_num: str, message: str) -> str:
        username = getpass.getuser()
        now = datetime.now().strftime("%Y%m%d")
        return f"--liquibase formatted sql\n\n--changeset {username}:{now}_{message}_{version_num}\n"

    @staticmethod
    def get_version_number_from_name(filename: Path) -> int:
        return int(filename.name.split("_")[1])

    def parse_message(self) -> None:
        self.message = re.sub(r"\s+", "_", self.message)
        self.message = re.sub(r"\-+", "_", self.message)

    def get_all_version_files(self) -> List[Path]:
        return sorted(self.migrate_location.glob("*.sql"), key=self.get_version_number_from_name)

    def _get_last_version_num(self) -> int:
        last_version_migration = self.get_all_version_files()
        if not last_version_migration:
            return 0
        return self.get_version_number_from_name(last_version_migration[-1])

    def generate_version(self, message: str) -> str:
        now = datetime.now().strftime("%Y%m%d").replace("/", "")
        last_version_num = self._get_last_version_num()
        version_num = f"{last_version_num + 1:04d}"
        migration_hash = hashlib.shake_128(str.encode(f"{uuid4()}")).hexdigest(3)
        return f"{now}_{version_num}_{message}_{migration_hash}.sql"

    def write_version_file(self) -> None:
        migrations = self.get_all_version_files()
        migrations = [
            MIGRATION_TEMPLATE.format(filename=filename.relative_to("migrations"))  # type: ignore
            for filename in migrations
        ]
        xml_changelog = CHANGELOG_XML_TEMPLATE.format("\n                   ".join(migrations))  # type: ignore
        Path("migrations/changelog.xml").write_text(xml_changelog)

    def generate_file_name(self) -> str:
        self.parse_message()
        return self.generate_version(message=self.message)

    def make_migration(self) -> None:
        file_name = self.generate_file_name()
        open(f"{self.migrations_path}/{file_name}", "w").close()
        self.write_version_file()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--message", dest="message", type=str, help="Message")
    parsed = parser.parse_args()
    if not parsed.message:
        raise KeyboardInterrupt("You need pass -m or --message")
    migrator = MakeMigration(migrations_path="migrations/sql", message=parsed.message)
    migrator.make_migration()
