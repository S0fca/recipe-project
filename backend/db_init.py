from db_connection import get_connection

def init_db():
    db = get_connection()
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

    cursor.execute("""
           CREATE OR REPLACE VIEW view_recipe_details AS
           SELECT 
               r.id AS recipe_id,
               r.title AS recipe_title,
               r.description AS recipe_description,
               r.difficulty,
               r.is_vegetarian,
               r.created_at,
               GROUP_CONCAT(CONCAT(i.name, ':', ri.amount, ri.unit) SEPARATOR ', ') AS ingredients
           FROM recipe r
           LEFT JOIN recipe_ingredient ri ON r.id = ri.recipe_id
           LEFT JOIN ingredient i ON ri.ingredient_id = i.id
           GROUP BY r.id
       """)

    cursor.execute("""
    CREATE OR REPLACE VIEW view_cookbook_summary AS
    SELECT 
        c.id AS cookbook_id,
        c.name AS cookbook_name,
        c.description AS cookbook_description,
        COUNT(rc.recipe_id) AS recipe_count
    FROM cookbook c
    LEFT JOIN recipe_cookbook rc ON c.id = rc.cookbook_id
    GROUP BY c.id, c.name, c.description
    """)

    db.commit()
    print("Database initialized.")
    cursor.close()
    db.close()
