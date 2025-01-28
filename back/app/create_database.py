import mysql.connector
import requests

# this should come from a .env file
connection = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="yourpassword",
    charset="utf8mb4",
    collation="utf8mb4_unicode_ci"
)
cursor = connection.cursor()

cursor.execute("DROP DATABASE IF EXISTS pokemon")
cursor.execute("CREATE DATABASE IF NOT EXISTS pokemon")
cursor.execute("USE pokemon")

cursor.execute("""
CREATE TABLE IF NOT EXISTS pokemon (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    height INT,
    weight INT,
    base_experience INT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS type (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS language (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(25) NOT NULL,
    code VARCHAR(10) NOT NULL UNIQUE
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS type_translation (
    id INT PRIMARY KEY AUTO_INCREMENT,
    type_id INT,
    language_id INT,
    translation VARCHAR(100) NOT NULL,
    FOREIGN KEY (type_id) REFERENCES type(id) ON DELETE CASCADE,
    FOREIGN KEY (language_id) REFERENCES language(id) ON DELETE CASCADE,
    UNIQUE KEY unique_type_lang (type_id, language_id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS pokemon_type (
    pokemon_id INT,
    type_id INT,
    PRIMARY KEY (pokemon_id, type_id),
    FOREIGN KEY (pokemon_id) REFERENCES pokemon(id) ON DELETE CASCADE,
    FOREIGN KEY (type_id) REFERENCES type(id) ON DELETE CASCADE
)
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS habilities (
        id INT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(255) NOT NULL,
        effect VARCHAR(255) NOT NULL
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS pokemon_habilities (
        pokemon_id INT,
        habilities_id INT,
        PRIMARY KEY (pokemon_id, habilities_id),
        FOREIGN KEY (pokemon_id) REFERENCES pokemon(id) ON DELETE CASCADE,
        FOREIGN KEY (habilities_id) REFERENCES habilities(id) ON DELETE CASCADE
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS habilities_translation (
        id INT PRIMARY KEY AUTO_INCREMENT,
        habilities_id INT,
        language_id INT,
        translation VARCHAR(100) NOT NULL,
        FOREIGN KEY (habilities_id) REFERENCES habilities(id) ON DELETE CASCADE,
        FOREIGN KEY (language_id) REFERENCES language(id) ON DELETE CASCADE,
        UNIQUE KEY unique_habilities_lang (habilities_id, language_id)
    )
""")

cursor.execute("""
			CREATE TABLE IF NOT EXISTS stats (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    name VARCHAR(255) NOT NULL
                )
                """) 

cursor.execute("""
			CREATE TABLE IF NOT EXISTS pokemon_stats (
                        pokemon_id INT,
                        stats_id INT,
                        value INT,
                        PRIMARY KEY (pokemon_id, stats_id),
                        FOREIGN KEY (pokemon_id) REFERENCES pokemon(id) ON DELETE CASCADE,
                        FOREIGN KEY (stats_id) REFERENCES stats(id) ON DELETE CASCADE
                    )
                    """)


cursor.execute("""
			CREATE TABLE IF NOT EXISTS stats_translation (
                        id INT PRIMARY KEY AUTO_INCREMENT,
                        stats_id INT,
                        language_id INT,
                        translation VARCHAR(100) NOT NULL,
                        FOREIGN KEY (stats_id) REFERENCES stats(id) ON DELETE CASCADE,
                        FOREIGN KEY (language_id) REFERENCES language(id) ON DELETE CASCADE,
                        UNIQUE KEY unique_stats_lang (stats_id, language_id)
                    )
                    """)

cursor.execute("""
			CREATE TABLE IF NOT EXISTS moves (
                        id INT PRIMARY KEY AUTO_INCREMENT,
                        name VARCHAR(255) NOT NULL,
                        accuracy INT,
                        pp INT,
                        power INT,
                        priority INT,
                        type_id INT,
                        FOREIGN KEY (type_id) REFERENCES type(id) ON DELETE CASCADE
                    )
                    """)

cursor.execute("""
            CREATE TABLE IF NOT EXISTS moves_translation (
                        id INT PRIMARY KEY AUTO_INCREMENT,
                        moves_id INT,
                        language_id INT,
                        translation VARCHAR(100) NOT NULL,
                        FOREIGN KEY (moves_id) REFERENCES moves(id) ON DELETE CASCADE,
                        FOREIGN KEY (language_id) REFERENCES language(id) ON DELETE CASCADE,
                        UNIQUE KEY unique_moves_lang (moves_id, language_id)
                    )
                    """)

cursor.execute("""
            CREATE TABLE IF NOT EXISTS pokemon_moves (
                        pokemon_id INT,
                        moves_id INT,
                        PRIMARY KEY (pokemon_id, moves_id),
                        FOREIGN KEY (pokemon_id) REFERENCES pokemon(id) ON DELETE CASCADE,
                        FOREIGN KEY (moves_id) REFERENCES moves(id) ON DELETE CASCADE
                    )
                    """)

# we can add games(generations) items evolutions(next and previous) and more the pokeapi has a lot of information
# move category i mean physical, special, status

languages = [
    ("English", "en"),
    ("Spanish", "es"),
    ("French",  "fr"),
    ("German",  "de")
]
cursor.executemany("INSERT INTO language (name, code) VALUES (%s, %s)", languages)

url = "https://pokeapi.co/api/v2/pokemon?limit=10"
pokemon_list = requests.get(url).json()["results"]

processed_types = set()

for pokemon in pokemon_list:
    details = requests.get(pokemon["url"]).json()
    name = details["name"]
    height = details["height"]
    weight = details["weight"]
    base_experience = details["base_experience"]

    cursor.execute(
        "INSERT INTO pokemon (name, height, weight, base_experience) VALUES (%s, %s, %s, %s)",
        (name, height, weight, base_experience)
    )
    pokemon_id = cursor.lastrowid

    types = details["types"]
    for type_entry in types:
        type_name = type_entry["type"]["name"]

        cursor.execute("SELECT id FROM type WHERE name = %s", (type_name,))
        row = cursor.fetchone()

        if not row:
            cursor.execute("INSERT INTO type (name) VALUES (%s)", (type_name,))
            type_id = cursor.lastrowid
        else:
            type_id = row[0]

        cursor.execute(
            "INSERT INTO pokemon_type (pokemon_id, type_id) VALUES (%s, %s)",
            (pokemon_id, type_id)
        )

        if type_name not in processed_types:
            processed_types.add(type_name)

            type_details = requests.get(f"https://pokeapi.co/api/v2/type/{type_name}").json()

            for translation_item in type_details['names']:
                language_code = translation_item['language']['name']
                if language_code in ["en", "es", "fr", "de"]:
                    cursor.execute(
                        "SELECT id FROM language WHERE code = %s",
                        (language_code,)
                    )
                    language_row = cursor.fetchone()
                    if language_row:
                        language_id = language_row[0]
                        cursor.execute("""
                            INSERT IGNORE INTO type_translation (type_id, language_id, translation)
                            VALUES (%s, %s, %s)
                        """, (type_id, language_id, translation_item['name']))

connection.commit()
cursor.close()
connection.close()

print("Datos cargados con éxito. Revisa tu BD para ver resultados.")
