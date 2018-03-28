import socket
import net
import os
from time import sleep
class server:
	def __init__(self):
		self.name = "SERVER_1"
		self.sock = socket.socket()
		self.host = socket.gethostname()
		self.port = 5000
		self.sock.bind(("192.168.83.132", 0))
		self.sock.connect(("192.168.83.143", self.port))
		while True:
			self.operations()

	def operations(self):
		msg = self.sock.recv(1024)
		if msg == 'WHO':
				self.sock.send('123123123*'+self.name)
		if '*' in msg:
			msg = msg.split('*')
			print "Query : ",msg
			if msg[0] == 'PREPARE':
				self.sock.send("READY")
				net.downloadFile(msg[1],self.sock)
				print "Chunk "+msg[1]+" is stored on "+self.name
			if msg[0] == 'MAKE':
				self.sock.send('READY?')
				sleep(1)
				net.uploadFile(msg[1],self.sock)
				#print "Chunk "+msg[1]+" is on mainserver by "+self.name
			if msg[0] == "DEL":
				print "Deletion Command received..",msg[1]
				if os.path.isfile(msg[1]):
					os.remove(msg[1])
					print "Deleted",msg[1]
				else:
					print msg[1],"File is not exists!!!!!!!!!"
server1 = server()
