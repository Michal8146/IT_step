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


cursor.execute("""
INSERT INTO users (username, name, email, password, address)
VALUES ('potato', 'Honza', 'brambora123@gmail.com', '123456', 'Pionyrska 10');""")

cursor.execute("""
SELECT
FROM users;""")


# save changes
conn.commit()


cursor.execute("select_query")
users = cursor.fetchall()

for user in users:
	print(user)
	



conn.close()