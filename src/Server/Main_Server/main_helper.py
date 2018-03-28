import socket
from time import sleep
import SQL as sq
from uploader import uploader
from downloader import downloader
from deleter import delete

def helper(client, sub_servers, C_lib):
  sql = sq.SQL()
  cursor = sql.getCursor()
  query = client["socket"].recv(1024)
  while query != '4':
    if query == '2':
      uploader(sql, client, sub_servers, C_lib)
    elif query == '1':
      downloader(sql, client, sub_servers, C_lib)
    elif query == '3':
      delete(sql, client, sub_servers, C_lib)
    sleep(1)
    print "Waiting for next command .."
    query = client["socket"].recv(1024)
    print 'Here is query ..',query
  client["socket"].close()
  print "End"
          
