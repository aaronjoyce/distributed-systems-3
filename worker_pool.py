import threading
import socket
from worker import Worker
from chat_room import ChatRoom

class WorkerPool:

	def __init__(self, host, port, thread_pool_size=20, buffer_size=1024):
		self.host = host 
		self.port = port 
		self.thread_pool_size = thread_pool_size
		self.buffer_size = buffer_size
		self.listener = None
		self.thread_pool = []
		self.chat_rooms = {'machine-learning':ChatRoom('machine-learning', 1, self.host, self.port)}

	def run(self):
		self.listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.listener.bind((self.host, self.port))
		self.listener.listen(1)

		while True:
			conn, addr = self.listener.accept()
			if (len(self.thread_pool) < self.thread_pool_size):
				# Then, accept the connection. 
				# Otherwise, return a full-capacity
				# message to the client attempting to 
				# connect.
				# At this point, we receive the data, getting
				# the name of the chatroom specified
				received = conn.recv(self.buffer_size)
				received_split = received.split('\n')
				action_key_value = received_split[0]
				action_name = action_key_value[:action_key_value.find(':')]
				if (action_name == 'JOIN_CHATROOM'):
					chat_room_name = action_key_value[action_key_value.find(':')+1:].strip()
					chat_room = self.chat_rooms[chat_room_name.strip()]
					client_name = None
					worker = Worker(addr[0], addr[1], conn, 1024, chat_room, client_name)
					worker.start()
					self.thread_pool.append(worker)
			else:
				print 'Oops, busy', addr

		return True