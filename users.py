import sqlite3
# Connect to the database
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# View all users
cursor.execute("SELECT id, username FROM users")
users = cursor.fetchall()

print("\nRegistered Users:")
for user in users:
    print(f"ID: {user[0]}, Username: {user[1]}")

conn.close()