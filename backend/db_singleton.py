import mysql.connector
import json
from pathlib import Path

class DatabaseConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance._connection = None
        return cls._instance

    def connect(self):
        if self._connection is None:
            config_path = Path(__file__).parent / "config.json"
            with open(config_path, "r") as file:
                config = json.load(file)["mysql"]

            self._connection = mysql.connector.connect(
                host=config["host"],
                user=config["user"],
                password=config["password"],
                database=config["database"]
            )
        return self._connection

    def close(self):
        if self._connection:
            self._connection.close()
            self._connection = None
