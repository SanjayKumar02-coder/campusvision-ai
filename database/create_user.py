import os
import sys
import sqlite3

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

from config import Config


connection = sqlite3.connect(Config.DATABASE)


users = [
    ("admin", "admin123", "admin"),
    ("faculty", "faculty123", "faculty"),
    ("student", "student123", "student")
]


for username, password, role in users:

    connection.execute("""
        INSERT OR IGNORE INTO users
        (username, password, role)
        VALUES (?, ?, ?)
    """, (username, password, role))


connection.commit()
connection.close()

print("All demo users created successfully!")