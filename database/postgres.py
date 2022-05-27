import os
from dataclasses import dataclass

import psycopg2


@dataclass
class PostgresConfig:
    PG_DATABASE = os.environ.get("PG_DATABASE", "postgres")
    PG_USER = os.environ.get("PG_USER", "postgres")
    PG_PASSWORD = os.environ.get("PG_PASSWORD", "docker")
    PG_HOST = os.environ.get("PG_HOST", "localhost")


class PostgresConnection(PostgresConfig):
    def __init__(self):
        self.connection = None

    def __enter__(self):
        try:
            print(self.PG_HOST)
            self.connection = psycopg2.connect(
                database=self.PG_DATABASE,
                user=self.PG_USER,
                password=self.PG_PASSWORD,
                host=self.PG_HOST,
                port=5432,
            )
            self.connection.autocommit = False
            return self.connection
        except psycopg2.DatabaseError as e:
            raise e
        except Exception as e:
            raise e

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_tb is None:
            self.connection.commit()
        else:
            self.connection.rollback()
        self.connection.close()
