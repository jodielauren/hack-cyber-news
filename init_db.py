import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO posts (title, content, url, category) VALUES (?, ?, ?, ?)",
            ('First Post', 'Content for the first post', 'url', 'category')
            )

cur.execute("INSERT INTO posts (title, content, url, category) VALUES (?, ?, ?, ?)",
            ('Second Post', 'Content for the second post', 'url', 'category')
            )

connection.commit()
connection.close()