# import sqlite3

# conn = sqlite3.connect('users.db')
# cursor = conn.cursor()
# cursor.execute("SELECT id, username FROM users")
# users = cursor.fetchall()
# print("\nRegistered Users:")
# for user in users:
#     print(f"ID: {user[0]}, Username: {user[1]}, Password: {user[2]}")
# conn.close()

import sqlite3
conn = sqlite3.connect('users.db')
cursor = conn.cursor()
cursor.execute("SELECT username, password FROM users")
users = cursor.fetchall()
print("\nRegistered Users:")
for user in users:
    print(f"Username: {user[0]}, Password: {user[1]}")
conn.close()