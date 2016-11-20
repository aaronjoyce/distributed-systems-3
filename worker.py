import threading
import socket
import chat_room
import time 

class Worker(threading.Thread):

	ACTION_JOIN_CHATROOM = 'JOIN_CHATROOM'
	ACTION_LEAVE_CHATROOM = 'LEAVE_CHATROOM'
	ACTION_DISCONNECT = 'DISCONNECT'
	ACTION_CHAT = 'CHAT'

	def __init__(self, host, port, socket, buffer_size=1024, chat_room=None, client_name=None, worker_pool=None):
		threading.Thread.__init__(self, target=self.run)
		self.host = host
 		self.port = port
		self.socket = socket
		self.exit = False
		self.buffer_size = buffer_size
		self.chat_rooms = {}
		self.chat_room_join_identifiers = {}
		self.last_chat_room_added = chat_room
		self.client_name = client_name
		self.worker_pool = worker_pool

	def get_client_name(self):
		return self.client_name

	def register_with_chatroom(self, chat_room):
		print chat_room
		self.chat_rooms[chat_room.get_identifier()] = chat_room
		self.chat_room_join_identifiers[chat_room.get_name()] = chat_room.register_observer(self)
		print self.chat_room_join_identifiers
		return self.chat_room_join_identifiers[chat_room.get_name()]

	def broadcast(self, message):
		print message
		self.socket.sendall(message)

	def get_chatroom(self):
		return self.chat_room

	def get_chat_room_join_identifier(self, chat_room_name):
		if chat_room_name in self.chat_room_join_identifiers:
			return self.chat_room_join_identifiers[chat_room_name]
		return False
	def deregister_with_chatroom(self, chat_room):
		return chat_room.deregister_observer(self)

	def disconnect(self):
		self.socket.close()
		# Then, terminate thread

	def run(self):
		self.register_with_chatroom(self.last_chat_room_added)
   		while not self.exit:
			print "waiting for data inside thread"
			print "CHAT_ROOM_IDENTIFIERS: " + str(self.chat_room_join_identifiers)
		  	received = self.socket.recv(1024)
			print "RECEIVED: " + received
			received_split = received.split('\n')
			action_key_value = received_split[0]
			action_name = action_key_value[:action_key_value.find(':')]
			if "helo" in received.strip().lower():
					print "received hello"
		   			self.socket.sendall("{0}\nIP:{1}\nPort:{2}\nStudentID:{3}\n\n".format(received.strip(), self.host, self.port, 12326755))
			elif "kill_service" in received.strip().lower():
					self.socket.close()
					self.exit = True
			elif (action_name == Worker.ACTION_LEAVE_CHATROOM):
				print "leaving chatroom"
				chat_room_identifier = int(action_key_value[action_key_value.find(':')+1:].strip())
				chat_room = self.chat_rooms[chat_room_identifier]

				self.socket.sendall("LEFT_CHATROOM: {0}\nJOIN_ID: {1}\n".format(chat_room_identifier, self.chat_room_join_identifiers[chat_room.get_name()]))
			#	self.deregister_with_chatroom(chat_room)
				chat_room.relay("{0} has left this chatroom.".format(self.get_client_name()), self)
				self.deregister_with_chatroom(chat_room)
			elif (action_name == Worker.ACTION_DISCONNECT):
				self.disconnect()
			elif (action_name == Worker.ACTION_CHAT):
				chat_room_identifier = int(action_key_value[action_key_value.find(':')+1:].strip())
				chat_room = self.chat_rooms[chat_room_identifier]
				message_key_value = received_split[2]
				message_content = message_key_value[message_key_value.find(':')+1:].strip()
				chat_room.relay(message_content, self)
			elif (action_name == 'JOIN_CHATROOM'):
				print "JOINING CHAT ROOM"
                          	chat_room_name = action_key_value[action_key_value.find(':')+1:].strip()
                           	client_name_key_value = received_split[3]
                           	client_name = client_name_key_value[client_name_key_value.find(':')+1:].strip()
				self.register_with_chatroom(self.worker_pool.chat_rooms[chat_room_name])
