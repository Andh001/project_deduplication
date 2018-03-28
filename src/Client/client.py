import os
import socket
import time
import net
import subprocess
sock = socket.socket()
host = "192.168.83.143"
port = 5000
sock.connect((host, port))
def getChecksum(filename):
	a = subprocess.Popen(['sha256sum',filename], stdout=subprocess.PIPE).communicate()[0]
	return a.split(' ')[0]
def Upload():
	choice = '0'
	while choice != 'n':
		filename = raw_input("Enter filename : ")
		while not os.path.isfile(filename):
			print filename+" is not exists,"
			filename = raw_input("Enter Filename : ")
		time.sleep(1)
		sock.send(getChecksum(filename)+'*'+filename)
		FLAG = sock.recv(1024)
		if FLAG == 'NOT_EXISTS':
			time.sleep(1)
			net.uploadFile(filename, sock)
		elif FLAG == 'FILE_EXISTS':
			print "File is already uploaded!"
		choice = raw_input("Upload another File?(y/n): ")
	time.sleep(1)
	sock.send('STOP_UPLOAD')

def Download(option):
	listt = sock.recv(1024)
	if listt != 'UPLOAD!':
		listt = listt.split('\n')
		for i in range(len(listt)):
			print i+1,".",listt[i]
		if option == "Download":
			no = raw_input("Enter File no to download the file : ")
			time.sleep(1)
			sock.send(no)
			net.downloadFile(listt[int(no)-1], sock)
		else:
			no = raw_input("Enter File no to Delete the file : ")
			time.sleep(1)
			sock.send(no)
	else:
		print "You are a new user!\nUpload some files then continue!"

username = raw_input("Enter username : ")
time.sleep(1)
sock.send(username)
choice = raw_input("1. Upload\n2. Download\n3.Delete File\n4. Logout\n :")
while choice != '4':
	time.sleep(1)
	sock.send(choice)
	if choice == '1':
		Upload()
	elif choice == '2':
		Download("Download")
	elif choice == '3':
		Download("Delete")
	time.sleep(1)
	choice = raw_input("1. Upload\n2. Download\n3.Delete File\n4. Logout\n :")
sock.send('4')
sock.close()
print "End"
