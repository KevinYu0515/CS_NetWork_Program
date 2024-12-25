class MessageManager:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = conn.cursor()

    def create_tables(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS message (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject_id INTEGER,
            content TEXT NOT NULL,
            user_id INTEGER,
            created_time DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (subject_id) REFERENCES subject (id),
            FOREIGN KEY (user_id) REFERENCES user (id)
        )
        ''')
        self.conn.commit()

    def add_message(self, subject_name, content, user_name):
        self.cursor.execute('''
            INSERT INTO message (subject_id, content, user_id)
            SELECT s.id, ?, u.id
            FROM subject s
            JOIN user u ON u.name = ?
            WHERE s.name = ?
        ''', (content, user_name, subject_name))
        self.conn.commit()

    def get_messages(self):
        self.cursor.execute('SELECT * FROM message')
        return self.cursor.fetchall()

    def update_message(self, message_id, new_content):
        self.cursor.execute('UPDATE message SET content = ? WHERE id = ?', (new_content, message_id))
        self.conn.commit()

    def delete_message(self, message_id):
        self.cursor.execute('DELETE FROM message WHERE id = ?', (message_id,))
        self.conn.commit()

    def get_messages_by_subject(self, subject_name):
        self.cursor.execute('''
        SELECT m.id as id, u.name as name, m.content as message, m.created_time as created_time  FROM message m
        JOIN subject s ON m.subject_id = s.id
        JOIN user u ON m.user_id = u.id
        WHERE s.name = ?
        ''', (subject_name,))
        return self.cursor.fetchall()
