import mysql.connector
import requests

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
