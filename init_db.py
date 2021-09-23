import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO posts (title, content, url) VALUES (?, ?, ?)",
            ('First Post', 'Content for the first post', 'url')
            )

cur.execute("INSERT INTO posts (title, content, url) VALUES (?, ?, ?)",
            ('Second Post', 'Content for the second post', 'url')
            )

connection.commit()
connection.close()