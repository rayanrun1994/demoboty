import sqlite3
# إذا لم يكن الملف موجودًا سيتم إنشاؤه تلقائيًا
conn = sqlite3.connect("ai_database.db")
# إنشاء كائن مؤشر (cursor) للتعامل مع قاعدة البيانات
cursor = conn.cursor()

# إنشاء جدول باسم "users" يحتوي على عمود id واسم وemail
def install_tabeles():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_user TEXT NOT NULL UNIQUE,
        name TEXT NOT NULL UNIQUE
    )
    """)
    conn.commit()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chat TEXT NOT NULL,
        role_type TEXT NOT NULL,
        id_chat INT NOT NULL,
        id_user INT NOT NULL
        
    )
    """)
    conn.commit()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS new_chat (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        name_ai TEXT NOT NULL,
        id_user INT NOT NULL
        
    )
    """)
    conn.commit()
install_tabeles()
class save_chat:
    def __init__(self, text_chat="", id_chat="", id_user="", role=""):
        self.text_chat = text_chat
        self.id_chat = id_chat
        self.id_user = id_user
        self.role = role
    def save(self):
        cursor.execute("""
        INSERT INTO messages (chat, role_type, id_chat, id_user)
        VALUES (?, ?, ?, ?)
        """, (self.text_chat, self.role, self.id_chat, self.id_user))
        conn.commit()
    def new_chat(self, name, name_ai, id_user):
        cursor.execute("""
        INSERT INTO new_chat (name, name_ai, id_user)
        VALUES (?, ?, ?)
        """, (name, name_ai, id_user))
        conn.commit()
class new_users():
    def __init__(self, id_user, name):
        self.id_user = id_user
        self.name = name
    def save(self):
        try:
            cursor.execute("""
            INSERT INTO users (id_user, name)
            VALUES (?, ?)
            """, (self.id_user, self.name))
            conn.commit()
        except:
            pass
class select:
    def __init__(self, id_user="", id_chat="", name=""):
        self.id_user = id_user
        self.id_chat = id_chat
        self.name = name
    def select(self):
        cursor.execute("""
        SELECT * FROM users WHERE id_user = ?
        """, (self.id_user,))
        result = cursor.fetchone()
        if result is None:
            return None
        else:
            return result
    def select_chats(self):
        cursor.execute("""
             SELECT * FROM new_chat WHERE id_user = ?
        """, (self.id_user,))
        results = cursor.fetchall()
        if len(results) == 0:
            return False
        else:
            return results
    def select_chat_one(self):
        cursor.execute("""
             SELECT * FROM new_chat WHERE id_user = ? AND name = ?
        """, (self.id_user, self.name))
        results = cursor.fetchone()
        if results is None:
            return False
        else:
            return results
    def messages(self):
        cursor.execute("""
            SELECT * FROM messages WHERE id_chat = ? AND id_user = ? ORDER BY id ASC
        """, (self.id_chat, self.id_user))
        results = cursor.fetchall()
        if len(results) == 0:
            return False
        else:
            return results
