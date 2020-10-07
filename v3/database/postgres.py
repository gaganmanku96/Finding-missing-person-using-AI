from dataclasses import dataclass

import psycopg2


@dataclass
class PostgresConfig():
    PG_DATABASE: str = "postgres"
    PG_USER: str = "postgres"
    PG_PASSWORD: str = "docker"
    PG_HOST: str = "localhost"


class PostgresConnection(PostgresConfig):
    def __init__(self):
        self.connection = None

    def __enter__(self):
        try:
            self.connection = psycopg2.connect(
                database=self.PG_DATABASE,
                user=self.PG_USER,
                password=self.PG_PASSWORD,
                host=self.PG_HOST
            )
            self.connection.autocommit = False
            return self.connection
        except:
            raise psycopg2.DatabaseError("Couldn' connect to Postgres Database")
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_tb is None:
            self.connection.commit()
        else:
            self.connection.rollback()
        self.connection.close()
