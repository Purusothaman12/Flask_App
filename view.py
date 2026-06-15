import sqlite3

conn = sqlite3.connect("instance/event_datbase.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM event")
print(cursor.fetchall())

conn.close()