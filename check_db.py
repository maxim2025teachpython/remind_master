import sqlite3

conn = sqlite3.connect("reminders.db")
cur = conn.cursor()

cur.execute("SELECT id, chat_id, text, run_date FROM reminders")
rows = cur.fetchall()

print("Содержимое базы:")
for row in rows:
    print(row)

conn.close()
