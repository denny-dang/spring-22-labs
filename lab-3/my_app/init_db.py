import sqlite3

newSampleId = "the_key"

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO samples (key, value, message) VALUES (?, ?, ?)",
            (newSampleId, 'sampleKey', 'success')
            )

connection.commit()
connection.close()