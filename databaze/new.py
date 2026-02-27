import sqlite3

# connect to database (creates it if it doesn't exist)
conn = sqlite3.connect("mydatabase.db")
cursor = conn.cursor()

# create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    address TEXT
);
""")


#cursor.execute("""
#INSERT INTO users (username, name, email, password, address)
#VALUES ('potato', 'pepik', 'pepa@gmail.com', 'heslotajny', 'Pionyrska 12');""")


# save changes


cursor.execute("""
UPDATE users
SET name = 'stepan'
WHERE id = 1;""")

conn.commit()


cursor.execute("""SELECT *
FROM users;""")
users = cursor.fetchall()

for user in users:
	print(user)
	

cursor.execute("""SELECT name
FROM users;""")
users = cursor.fetchall()

for user in users:
	print(user)
	



conn.close()