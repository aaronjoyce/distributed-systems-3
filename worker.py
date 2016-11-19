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
		self.chat_rooms = {}
		self.chat_room_join_identifiers = {}
		self.client_name = client_name
		self.register_with_chatroom(chat_room)

	def get_client_name(self):
		return self.client_name

	def register_with_chatroom(self, chat_room):
		self.chat_rooms[chat_room.get_identifier()] = chat_room
		self.chat_room_join_identifiers[chat_room.get_name()] = chat_room.register_observer(self)
		return self.chat_room_join_identifiers[chat_room.get_name()]

	def broadcast(self, message):
		self.socket.sendall(message)

	def get_chatroom(self):
		return self.chat_room

	def get_chat_room_join_identifier(self, chat_room_name):
		return self.chat_room_join_identifiers[chat_room_name]

	def deregister_with_chatroom(self, chat_room):
		return chat_room.deregister_observer(self)

	def disconnect(self):
		self.socket.close()
		# Then, terminate thread

	def run(self):
   		while not self.exit:
		  	received = self.socket.recv(self.buffer_size)
			received_split = received.split('\n')
			action_key_value = received_split[0]
			action_name = action_key_value[:action_key_value.find(':')]
			if (action_name == Worker.ACTION_LEAVE_CHATROOM):
				chat_room_identifier = int(action_key_value[action_key_value.find(':')+1:].strip())
				chat_room = self.chat_rooms[chat_room_identifier]
				self.deregister_with_chatroom(chat_room)
				self.socket.sendall("LEFT_CHATROOM: {0}\nJOIN_ID: {1}\n".format(chat_room_identifier, self.chat_room_join_identifiers[chat_room.get_name()]))
			elif (action_name == Worker.ACTION_DISCONNECT):
				self.disconnect()
			elif (action_name == Worker.ACTION_CHAT):
				chat_room_identifier = int(action_key_value[action_key_value.find(':')+1:].strip())
				chat_room = self.chat_rooms[chat_room_identifier]
				message_key_value = received_split[3]
				message_content = message_key_value[message_key_value.find(':')+1:].strip()
				print "message_content: " + str(message_content)
				chat_room.relay(message_content, self)
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
