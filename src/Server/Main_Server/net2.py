import socket
import time
def dataa_downloadFile(filename, sock):
	buff = ""
	print "========>",filename
	sock.send("MAKE*"+filename)
	if sock.recv(100) == "READY?":
		sock.send("READY!")
		bytes = sock.recv(1024)
		while bytes != 'FIN':
			buff += bytes
			bytes = sock.recv(1024)
	return buff

