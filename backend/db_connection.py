import mysql.connector
import json
from pathlib import Path

def get_connection():
    config_path = Path(__file__).parent / "config.json"
    try:
        with open(config_path, "r") as file:
            config = json.load(file)["mysql"]
    except FileNotFoundError:
        print(f"Error: Config file not found at {config_path}")
        return None
    except KeyError:
        print("Error: 'mysql' section missing in config file")
        return None
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in config file: {e}")
        return None

    try:
        conn = mysql.connector.connect(
            host=config["host"],
            user=config["user"],
            password=config["password"],
            database=config["database"]
        )
        return conn
    except mysql.connector.Error as err:
        if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
            print("Error: Access denied. Check your username and password.")
        elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
            print(f"Error: Database '{config['database']}' does not exist.")
        else:
            print(f"Database connection error: {err}")
        return None