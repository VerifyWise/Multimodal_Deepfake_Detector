import sqlite3

DB_NAME = "users.db"


def view_users():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM users")
    users = c.fetchall()
    conn.close()

    if users:
        for user in users:
            print(f"ID: {user[0]}, Username: {user[1]}, Password: {user[2]}")
    else:
        print("No users found in the database.")


view_users()
