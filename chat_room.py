import threading
import socket

class ChatRoom:

	def __init__(self, name, identifier, host='localhost', port=8080):
		self.name = name
		self.identifier = identifier
		self.observers = {}
		self.host = host
		self.port = port

	def register_observer(self, observer):
		worker_identifier = len(self.observers)
		self.observers[worker_identifier] = observer

		observer.broadcast(
			"JOINED_CHATROOM: {0}\nSERVER_IP: {1}\nPORT: {2}\nROOM_REF: {3}\nJOIN_ID: {4}\n".format(
				self.get_name(), 
				self.get_host(), 
				self.get_port(), 
				self.get_identifier(), 
				worker_identifier))
		return worker_identifier

	def deregister_observer(self, observer):
		del self.observers[observer.get_chat_room_join_identifier(self.get_name())]

	def get_name(self):
		return self.name

	def get_host(self):
		return self.host 

	def get_port(self):
		return self.port

	def get_identifier(self):
		return self.identifier

	def relay(self, message_content, relayer):
		for key in self.observers:
			# request that they relay the message to listening client
			observer = self.observers[key]
			observer.broadcast("CHAT: {0}\nCLIENT_NAME: {1}\nMESSAGE: {2}\n".format(self.get_identifier(), relayer.get_client_name(), message_content))
