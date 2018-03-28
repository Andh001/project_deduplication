import socket
from time import sleep
from threading import Thread
from main_helper import helper
import ctypes

MAX_SERVERS = 5

C = ctypes.CDLL('./RAM.so')
C.ii()
hostname = "192.168.83.143"
port = 5000
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

sock.bind((hostname, port))
sock.listen(MAX_SERVERS)

class MAIN:
  def __init__(self):
    print "STARTED MAIN SERVER"
    self.servers = 0
    self.socks = [[],[]]
    self.password = "123123123"
    self.flag = 0

  def authenticate(self,client):
    username = client["socket"].recv(1024)
    client["username"] = username
    return 1

  def for_one_client(self, client):
    helper(client, self.socks,C)

  def service(self):
    print "Waiting for clients"
    c = MAX_SERVERS
    while c != 0:
      mini_sock, addr = sock.accept()
      client = {"socket":""}
      print "Client connection from:", addr
      client["socket"] = mini_sock
      if self.authenticate(client): # this is demo authentication
        Thread(target=self.for_one_client, args=(client,)).start()

  def add_servers(self, mini_sock, mini_sock_addr,idd,ip):
    self.socks[0] += [mini_sock]
    self.socks[1] += [ip]
    print self.socks
    print "Added Server ",ip
    if self.servers == MAX_SERVERS and self.flag == 0:
      self.flag = 1
      print "Main Server is ready"
      sock.listen(10)
      Thread(target=self.service, args=()).start()

M = MAIN()

while M.flag == 0:
  print "Waiting for "+str(MAX_SERVERS-M.servers)+" servers..."
  mini_sock, addr = sock.accept()
  #print "... connection from:", addr

  mini_sock.send("WHO")
  sleep(1)
  ans= mini_sock.recv(1024)
  if '*' in ans:
	idd = ans.split('*')
	if M.password == idd[0]:
	  M.servers += 1
	  Thread(target=M.add_servers, args=(mini_sock,addr,idd[-1],addr[0],)).start()
	  sleep(1)

