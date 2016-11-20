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
			"JOINED_CHATROOM:{0}\nSERVER_IP: {1}\nPORT: {2}\nROOM_REF: {3}\nJOIN_ID: {4}\n".format(
				self.get_name(), 
				self.get_host(), 
				self.get_port(), 
				self.get_identifier(), 
				worker_identifier))
		self.relay("{0} has joined this chatroom.".format(observer.get_client_name()), observer)
		return worker_identifier

	def deregister_observer(self, observer):
		print self.observers
		if observer.get_chat_room_join_identifier(self.get_name()) in self.observers:
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
		print "MESSAGE RELAYED: " + message_content
		relayer.broadcast("CHAT:{0}\nCLIENT_NAME:{1}\nMESSAGE:{2}\n".format(self.get_identifier(), relayer.get_client_name(), message_content))
		for key in self.observers:
			relayer_key = relayer.get_chat_room_join_identifier(self.get_name())
			if (relayer_key and (key == relayer_key)):
				continue
			# request that they relay the message to listening client
			observer.broadcast("CHAT:{0}\nCLIENT_NAME:{1}\nMESSAGE:{2}\n\n".format(self.get_identifier(), relayer.get_client_name(), message_content))
