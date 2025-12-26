from db_singleton import DatabaseConnection

def init_db():
    db = DatabaseConnection().connect()
    cursor = db.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS recipe (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(150) NOT NULL,
            description TEXT,
            difficulty ENUM('easy','medium','hard') NOT NULL,
            is_vegetarian BOOLEAN NOT NULL DEFAULT FALSE,
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ingredient (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL UNIQUE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS recipe_ingredient (
            recipe_id INT NOT NULL,
            ingredient_id INT NOT NULL,
            amount FLOAT NOT NULL,
            unit VARCHAR(20) NOT NULL,
            PRIMARY KEY (recipe_id, ingredient_id),
            FOREIGN KEY (recipe_id) REFERENCES recipe(id) ON DELETE CASCADE,
            FOREIGN KEY (ingredient_id) REFERENCES ingredient(id) ON DELETE CASCADE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cookbook (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            description TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS recipe_cookbook (
            recipe_id INT NOT NULL,
            cookbook_id INT NOT NULL,
            PRIMARY KEY (recipe_id, cookbook_id),
            FOREIGN KEY (recipe_id) REFERENCES recipe(id) ON DELETE CASCADE,
            FOREIGN KEY (cookbook_id) REFERENCES cookbook(id) ON DELETE CASCADE
        )
    """)

    db.commit()
    cursor.close()
    print("Database initialized")
