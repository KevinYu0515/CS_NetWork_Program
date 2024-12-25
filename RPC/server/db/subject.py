class SubjectManager:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = conn.cursor()

    def create_tables(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS subject (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            created_time DATETIME DEFAULT CURRENT_TIMESTAMP,
            created_user_id INTEGER,
            FOREIGN KEY (created_user_id) REFERENCES user (id)
        )
        ''')
        self.conn.commit()

    def add_subject(self, name, description, created_name):
        self.cursor.execute('''
        INSERT INTO subject (name, description, created_user_id)
        VALUES (
            ?, 
            ?,
            (SELECT id FROM user WHERE name = ?)
        )
        ''', (name, description, created_name))
        self.conn.commit()

    def get_subjects(self):
        self.cursor.execute('''
        SELECT 
            subject.id as id, 
            subject.name as name, 
            subject.description as description, 
            user.name AS created_user,
            subject.created_time as created_time
        FROM 
            subject
        LEFT JOIN 
            user ON subject.created_user_id = user.id;
        ''')
        return self.cursor.fetchall()

    def update_subject(self, subject_id, new_name, new_description):
        self.cursor.execute('UPDATE subject SET name = ?, description = ? WHERE id = ?', (new_name, new_description, subject_id))
        self.conn.commit()

    def delete_subject(self, subject_id):
        self.cursor.execute('''
                SELECT COUNT(*) FROM message 
                WHERE subject_id = ?
            ''', (subject_id,))
        message_count = self.cursor.fetchone()[0]
        if message_count > 0:
            return False
        
        self.cursor.execute('''
                DELETE FROM subject 
                WHERE id = ?
            ''', (subject_id,))
        self.conn.commit()
        return True

    def subject_exists(self, name):
        self.cursor.execute('SELECT * FROM subject WHERE name = ?', (name,))
        return self.cursor.fetchone() is not None
    
    def check_subject(self, subject_id, username):
        print(subject_id, username)
        self.cursor.execute('''
                SELECT 
                    EXISTS (
                        SELECT *
                        FROM subject as s
                        JOIN user as u ON s.created_user_id = u.id
                        WHERE s.id = ? 
                        AND u.name = ?
                    ) AS res;
            ''', (subject_id, username, ))
        return self.cursor.fetchall()
