import socket
import ctypes
import time
import chunks_manager
from threading import Thread

def _sub_del(sock, c_checksum):
  sock.send("DEL*"+c_checksum)


def p(n1):
  print "Here",n1
  time.sleep(4)

def delete(sql, client, sub_servers, C_lib):
  names = sql.MakeList(client)
  c = 0
  if names == 0:
    client["socket"].send('UPLOAD!')
  else:
    listt = '\n'.join(x[0] for x in names)
    client["socket"].send(listt)
    no = client["socket"].recv(10)
    print "Here is filename user want to delete...",no,names[int(no)-1][0]
    #c = sql.exeq('select count(m_checksum) from log where m_checksum="%s"'%(names[int(no)-1][1])) not working...???
    c = sql.exeq('select c_checksum from 256kb_chunks where m_checksum="%s" limit 1'%(names[int(no)-1][1]))
    sql.exeq('delete from log where username="%s" and filename="%s";' %(client["username"], names[int(no)-1][0]))
    r = sql.exeq('select c_checksum from 256kb_chunks where m_checksum = "%s"'%(names[int(no)-1][1]))
    c = ctypes.c_int(C_lib.GET_COUNT(ctypes.c_char_p(c[0][0])))
    c = c.value
    if c == 1:
      sql.exeq('delete from 256kb_chunks where m_checksum="%s"'%(names[int(no)-1][1]))
    for i in r:
      print "]]]]]]]]]]]]]>>>>>",c
      if c == 1:
        print "HERERE",i[0]
        ips = ctypes.c_wchar_p(C_lib.SEARCH_NODE(ctypes.c_char_p(i[0])))
        ipss = chunks_manager.intoip(ips.value)
        print "---------->>>>>> ips from deleter.py", ipss
        for j in ipss: 
          print "Created deletion Thread to",j
          Thread(target=_sub_del, args=(sub_servers[0][sub_servers[1].index(j)],i[0],)).start()
      oo = ctypes.c_int(C_lib.GET_COUNT(ctypes.c_char_p(i[0])))
      print "Count of",i[0],"is",oo.value
      g = ctypes.c_int(C_lib.DEC_COUNT(ctypes.c_char_p(i[0])))
      oo = ctypes.c_int(C_lib.GET_COUNT(ctypes.c_char_p(i[0])))
      print "decreased of",i[0],"is",oo.value
      if g.value == 1:
        print "Successfully decreased count of",i[0]
        if oo.value == 0:
          sql.exeq('delete from 256kb_chunks where m_checksum="%s"'%(names[int(no)-1][1]))
          ips = ctypes.c_wchar_p(C_lib.SEARCH_NODE(ctypes.c_char_p(i[0])))
          ipss = chunks_manager.intoip(ips.value)
          print "~~~~~~~~}}} ips from deleter.py", ipss
          for j in ipss: 
            print "Created deletion Thread to",j
            Thread(target=_sub_del, args=(sub_servers[0][sub_servers[1].index(j)],i[0],)).start()
      else:
        print "Failed to decrease count of",i[0]
    sql.exeq('commit')
    print "Ended deletion..."
  return
