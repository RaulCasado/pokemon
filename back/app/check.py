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
cursor.execute("USE pokemon")

# Verificar las tablas existentes
cursor.execute("SHOW TABLES")
tables = cursor.fetchall()
print("Tablas existentes:")
for table in tables:
    print(f"- {table[0]}")

# Verificar los datos en la tabla `pokemon`
print("\nDatos en la tabla 'pokemon':")
cursor.execute("SELECT * FROM pokemon LIMIT 10")
pokemon_rows = cursor.fetchall()
for row in pokemon_rows:
    print(row)

# Verificar los datos en la tabla `types`
print("\nDatos en la tabla 'types':")
cursor.execute("SELECT * FROM type LIMIT 10")
types_rows = cursor.fetchall()
for row in types_rows:
    print(row)

# Verificar los datos en la tabla `type_translations`
print("\nDatos en la tabla 'type_translations':")
cursor.execute("SELECT * FROM type_translation LIMIT 10")
type_translations_rows = cursor.fetchall()
for row in type_translations_rows:
    print(row)
    
# Verificar los datos en la tabla `pokemon_type`
print("\nDatos en la tabla 'pokemon_type':")
cursor.execute("SELECT * FROM pokemon_type LIMIT 10")
pokemon_type_rows = cursor.fetchall()
for row in pokemon_type_rows:
	print(row)


query = """
SELECT p.name AS pokemon_name,
       tt.translation AS type_translation,
       l.code AS language_code
FROM pokemon p
JOIN pokemon_type pt ON p.id = pt.pokemon_id
JOIN type_translation tt ON pt.type_id = tt.type_id
JOIN language l ON tt.language_id = l.id
WHERE l.code = 'es'
ORDER BY p.id
"""

cursor.execute(query)
results = cursor.fetchall()

print("Pokémon y sus tipos en inglés:")
for (pokemon_name, type_translation, language_code) in results:
    print(f"Pokémon: {pokemon_name}, Tipo: {type_translation} ({language_code})")

# Cerrar la conexión
cursor.close()
connection.close()
