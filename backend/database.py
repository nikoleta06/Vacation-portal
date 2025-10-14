import sqlite3

DB_NAME = "backend/database.db" # name file database 

# connect with database
conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

# table of users
cursor.execute(""" CREATE TABLE IF NOT EXISTS users (
               id INTEGER PRIMARY KEY AUTOINCREMENT, 
               name TEXT NOT NULL,
               email TEXT NOT NULL,
               role TEXT NOT NULL,
               password TEXT NOT NULL)""")


#table of vacation request
cursor.execute(""" CREATE TABLE IF NOT EXISTS vocation_requests ( 
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               user_id INTEGER NOT NULL, 
               start_date TEXT NOT NULL,
               end_date TEXT NOT NULL,
               reason TEXT,
               status TEXT DEFAULT 'pending',
               FOREIGN KEY(user_id) REFERENCES users(id))""")


conn.commit()
conn.close()


print("Database initialized successfully!")
