import mysql.connector
import json
from pathlib import Path

def get_connection():
    config_path = Path(__file__).parent / "config.json"
    with open(config_path, "r") as file:
        config = json.load(file)["mysql"]

    return mysql.connector.connect(
        host=config["host"],
        user=config["user"],
        password=config["password"],
        database=config["database"]
    )