import sqlite3

conn = sqlite3.connect("complaints.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS complaints (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    location TEXT,
    issue TEXT,
    status TEXT DEFAULT 'Pending',
    eta TEXT DEFAULT 'Not Available'
)
""")
conn.commit()

def save_complaint(location, issue):
    cursor.execute("INSERT INTO complaints (location, issue) VALUES (?, ?)", (location, issue))
    conn.commit()

def check_complaint(location):
    cursor.execute("SELECT * FROM complaints WHERE location LIKE ?", ('%'+location+'%',))
    return cursor.fetchall()
