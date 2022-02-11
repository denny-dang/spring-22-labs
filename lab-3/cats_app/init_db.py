import sqlite3
import uuid

newCatId = str(uuid.uuid4())

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO cats (id, catName, catColor, catBreed) VALUES (?, ?, ?, ?)",
            (newCatId, 'Fluffy', 'Black', 'Ragdoll',)
            )

connection.commit()
connection.close()