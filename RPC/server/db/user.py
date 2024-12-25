class UserManager:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = conn.cursor()

    def create_tables(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
        ''')
        self.conn.commit()

    def add_user(self, name):
        self.cursor.execute('INSERT INTO user (name) VALUES (?)', (name,))
        self.conn.commit()

    def get_users(self):
        self.cursor.execute('SELECT * FROM user')
        return self.cursor.fetchall()

    def update_user(self, user_id, new_name):
        self.cursor.execute('UPDATE user SET name = ? WHERE id = ?', (new_name, user_id))
        self.conn.commit()

    def delete_user(self, user_id):
        self.cursor.execute('DELETE FROM user WHERE id = ?', (user_id,))
        self.conn.commit()

    def user_exists(self, name):
        self.cursor.execute('SELECT * FROM user WHERE name = ?', (name,))
        return self.cursor.fetchone() is not None
