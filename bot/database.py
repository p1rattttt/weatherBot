import sqlite3

class SQL:
    database: str
    def __init__(self, base):
        self.database = base
        self.conn = sqlite3.connect(self.database, check_same_thread=False)
        self.cur = self.conn.cursor()
        self.cur.execute('''
                            CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            city VARCHAR(255)
                                )''')
        self.conn.commit()

    def add(self, id, city):
        if self.checkuser(id):
            self.delete(id)
        with self.conn:
            # self.cur = self.conn.cursor()
            self.cur.execute("INSERT INTO 'users' ('id', 'city') VALUES(?,?)", (id, city))
            self.conn.commit()

    def checkuser(self, id):
        with self.conn:
            # self.cur = self.conn.cursor()
            result = self.cur.execute('''
                SELECT * FROM users WHERE id = ?''', (id,)).fetchall()
            return bool(len(result))

    def delete(self, id):
        with self.conn:
            self.cur.execute("DELETE FROM users WHERE id=?", (id,)).fetchall()
            self.conn.commit()

    def getcity(self, id):
        with self.conn:
            # self.cur = self.conn.cursor()
            user = self.cur.execute("SELECT * FROM 'users' ")
            for i in user:
                return i[1]
