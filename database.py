import sqlite3
from config import DB_PATH


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER,
            text TEXT,
            run_date TEXT,
            repeat_type TEXT DEFAULT 'none',
            repeat_value INTEGER
        )
    """)

    try:
        cur.execute("ALTER TABLE reminders ADD COLUMN repeat_type TEXT DEFAULT 'none'")
    except:
        pass

    try:
        cur.execute("ALTER TABLE reminders ADD COLUMN repeat_value INTEGER")
    except:
        pass

    conn.commit()
    conn.close()


def add_reminder(chat_id, text, run_date, repeat_type, repeat_value):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO reminders (chat_id, text, run_date, repeat_type, repeat_value)
        VALUES (?, ?, ?, ?, ?)
    """, (chat_id, text, run_date, repeat_type, repeat_value))
    conn.commit()
    conn.close()


def update_reminder_time(reminder_id, new_time):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("UPDATE reminders SET run_date = ? WHERE id = ?", (new_time, reminder_id))
    conn.commit()
    conn.close()


def delete_reminder(reminder_id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DELETE FROM reminders WHERE id = ?", (reminder_id,))
    conn.commit()
    conn.close()


def get_user_reminders(chat_id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        SELECT id, text, run_date, repeat_type, repeat_value
        FROM reminders WHERE chat_id = ?
    """, (chat_id,))
    rows = cur.fetchall()
    conn.close()
    return rows


def load_all_reminders():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        SELECT id, chat_id, text, run_date, repeat_type, repeat_value
        FROM reminders
    """)
    rows = cur.fetchall()
    conn.close()
    return rows
