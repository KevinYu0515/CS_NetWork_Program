from xmlrpc.server import SimpleXMLRPCServer
from socketserver import ThreadingMixIn
from db import DatabaseManager
import threading

PORT = 8810

class ChatRoom:
	def __init__(self, db: DatabaseManager) -> None:
		self.db = db
		self.lock = threading.Lock()

	def register(self, name: str):
		with self.lock:
			if not self.db.get_user_manager().user_exists(name):
				self.db.get_user_manager().add_user(name)
				return f"The user '{name}' register successfully!"
			else:
				return f"NO! The user '{name}' is registered!"

	def create(self, name: str, description: str, created_user):
		with self.lock:
			if not self.db.get_subject_manager().subject_exists(name):
				self.db.get_subject_manager().add_subject(name, description, created_user)
				return f"The subject '{name}' build successfully!"
			return  f"The subject '{name}' is built!"

	def subject(self):
		return self.db.get_subject_manager().get_subjects()

	def reply(self, subject, message, username):
		with self.lock:
			self.db.get_message_manager().add_message(subject, message, username)
			return "Reply Success!"
	
	def discussion(self, subject):
		return self.db.get_message_manager().get_messages_by_subject(subject)

	def delete(self, subject):
		with self.lock:
			response = self.db.get_subject_manager().delete_subject(subject)
			return "Delete Success!" if response else "Delete Failed"

	def delete_msg(self, msg):
		with self.lock:
			self.db.get_message_manager().delete_message(msg)
			return "Delete Success!"
	
	def check_subject(self, subject_id, username):
		with self.lock:
			res = self.db.get_subject_manager().check_subject(subject_id, username)[0]
			print(res)
			return res[0]
			
				
				
		
class ThreadXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
	pass

def main():
	db = DatabaseManager()
	server = ThreadXMLRPCServer(('localhost', PORT))
	server.register_instance(ChatRoom(db))
	print('Listen on port  %d' % PORT)
	try:
		print('Use Control-C to exit!')
		server.serve_forever()
	except KeyboardInterrupt:
		print('Server exit')
		
if __name__ == '__main__':
	main()