import threading
import socket
import chat_room

class Worker(threading.Thread):

	ACTION_JOIN_CHATROOM = 'JOIN_CHATROOM'
	ACTION_LEAVE_CHATROOM = 'LEAVE_CHATROOM'
	ACTION_DISCONNECT = 'DISCONNECT'
	ACTION_CHAT = 'CHAT'

	def __init__(self, host, port, socket, buffer_size=1024, chat_room=None, client_name=None):
		threading.Thread.__init__(self, target=self.run)
		self.host = host
 		self.port = port
		self.socket = socket
		self.exit = False
		self.buffer_size = buffer_size
		self.chat_room = chat_room
		self.chat_room_join_identifier = None
		self.register_with_chatroom()
		self.client_name = client_name

	def get_client_name():
		return self.client_name

	def register_with_chatroom(self):
		self.chat_room_join_identifier = self.chat_room.register_observer(self)

	def broadcast(self, message):
		self.socket.sendall(message)

	def get_chatroom(self):
		return self.chat_room

	def get_chat_room_join_identifier(self):
		return self.chat_room_join_identifier

	def deregister_with_chatroom(self):
		return self.chat_room.deregister_observer(self)

	def disconnect(self):
		self.socket.close()
		# Then, terminate thread

	def run(self):
   		while not self.exit:
		  	received = self.socket.recv(self.buffer_size)

			received_split = received.split('\n')
			action_key_value = received_split[0]
			action_name = action_key_value[:action_key_value.find(':')]
			print action_name
			if (action_name == Worker.ACTION_LEAVE_CHATROOM):
				chat_room_identifier = action_key_value[action_key_value.find(':')+1:].strip()
				self.deregister_with_chatroom()
				self.socket.sendall("LEFT_CHATROOM: {0}\nJOIN_ID: {1}\n".format(chat_room_identifier, self.chat_room_join_identifier))
			elif (action_name == Worker.ACTION_DISCONNECT):
				self.disconnect()
			elif (action_name == Worker.ACTION_CHAT):
				print received
				message_key_value = received_split[2]
				message_content = message_key_value[message_key_value.find(':')+1:].strip()
				self.chat_room.relay(message_content, self)
			else:
				break
			"""
			switch (action_name):
				case Worker.ACTION_LEAVE_CHATROOM:
					self.deregister_with_chatroom()
					self.socket.sendall("LEAVING CHATROOM\nIP:{0}\nPort:{1}\nStudentID:{2}\n".format(self.host, self.port, 12326755))
					break
				case Worker.ACTION_DISCONNECT:
					self.disconnect()
					self.socket.sendall("HELO text\nIP:{0}\nPort:{1}\nStudentID:{2}\n".format(self.host, self.port, 12326755))
					break
				case Worker.ACTION_CHAT:
					self.chat_room.relay(received)
					break
				default:
					break
			"""
