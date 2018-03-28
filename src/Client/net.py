import os
import socket
import time
#this is original upload and download code is same for client and server
def uploadFile(filename, sock):
	if os.path.isfile(filename):
		with open(filename, 'rb') as F:
			bytes = F.read(1024)
			while bytes != '':
				sock.send(bytes)
				bytes = F.read(1024)
			time.sleep(1)
			sock.send('FIN')
		print "File Send"
	else:
		print "File is not exists"

def downloadFile(filename, sock):
	with open(filename, 'wb') as F:
		bytes = sock.recv(1024)
		while bytes != 'FIN':
			F.write(bytes)
			bytes = sock.recv(1024)
		print "File",filename,"Downloaded!"		

def data_downloadFile(filename, sock):
	buff = ""
	bytes = sock.recv(1024)
	while bytes != 'FIN':
		buff += bytes
		bytes = sock.recv(1024)
	return buff