import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO posts (title, content, url, category) VALUES (?, ?, ?, ?)",
            ('OAuth Device Code Flow Phishing attack', 'Check out this great demonstration (~5mins) of a cool phishing attack which was presented at DEFCON 29', 'https://youtu.be/4J4RT4oMYdA?t=893', 'cloudsec')
            )

cur.execute("INSERT INTO posts (title, content, url, category) VALUES (?, ?, ?, ?)",
            ('AWS IAM Priv Esc', 'Check out this interesting post...', 'https://labs.bishopfox.com/tech-blog/iam-vulnerable-an-aws-iam-privilege-escalation-playground', 'cloudsec')
            )

connection.commit()
connection.close()