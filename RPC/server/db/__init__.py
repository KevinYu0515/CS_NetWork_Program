import sqlite3
from .user import UserManager
from .subject import SubjectManager
from .message import MessageManager
from threading import local

class DatabaseManager:
    def __init__(self, db_name='example.db'):
        self.db_name = db_name
        self.local_data = local()

        self._initialize_tables()

    def _initialize_tables(self):
        temp_conn = sqlite3.connect(self.db_name)
        user_mgr = UserManager(temp_conn)
        subject_mgr = SubjectManager(temp_conn)
        message_mgr = MessageManager(temp_conn)

        user_mgr.create_tables()
        subject_mgr.create_tables()
        message_mgr.create_tables()

        temp_conn.close()

    def get_connection(self):
        if not hasattr(self.local_data, 'connection'):
            self.local_data.connection = sqlite3.connect(self.db_name, check_same_thread=False)
        return self.local_data.connection
    
    def get_user_manager(self):
            if not hasattr(self.local_data, 'user_mgr'):
                self.local_data.user_mgr = UserManager(self.get_connection())
            return self.local_data.user_mgr

    def get_subject_manager(self):
        if not hasattr(self.local_data, 'subject_mgr'):
            self.local_data.subject_mgr = SubjectManager(self.get_connection())
        return self.local_data.subject_mgr

    def get_message_manager(self):
        if not hasattr(self.local_data, 'message_mgr'):
            self.local_data.message_mgr = MessageManager(self.get_connection())
        return self.local_data.message_mgr

    def close(self):
        self.conn.close()
