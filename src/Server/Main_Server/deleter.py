import socket
import ctypes
import time
import chunks_manager
from threading import Thread

def _sub_del(sock, c_checksum):
  time.sleep(1)
  sock.send("DEL*"+c_checksum)
  time.sleep(1)


def p(n1):
  print "Here",n1
  time.sleep(4)

def delete(sql, client, sub_servers, C_lib):
  names = sql.MakeList(client)
  c = 0
  if names == 0:
    client["socket"].send('UPLOAD!')
  else:
    print names
    listt = '\n'.join(x[0] for x in names)
    client["socket"].send(listt)
    no = client["socket"].recv(10)
    print "Here is filename user want to delete...",no,names[int(no)-1][0]
    sql.exeq('delete from log where username="%s" and filename="%s";' %(client["username"], names[int(no)-1][0]))
    sql.exeq('commit')
    r = sql.exeq('select c_checksum from 256kb_chunks where m_checksum = "%s"'%(names[int(no)-1][1]))
    for i in r:
      c = ctypes.c_int(C_lib.GET_COUNT(ctypes.c_char_p(i[0])))
      if c.value == 1:
        ips = ctypes.c_wchar_p(C_lib.SEARCH_NODE(ctypes.c_char_p(i[0])))
        ipss = chunks_manager.intoip(ips.value)
        for j in ipss: 
          print "Created deletion Thread to",j
          Thread(target=_sub_del, args=(sub_servers[0][sub_servers[1].index(j)],i[0],)).start()
        #sql.exeq('delete from 256kb_chunks where c_checksum="%s" and m_checksum="%s"'%(i[0],names[int(no)-1][1]))
        #sql.exeq('commit')
      sql.exeq('commit')#else:
      g = ctypes.c_int(C_lib.DEC_COUNT(ctypes.c_char_p(i[0])))
      oo = ctypes.c_int(C_lib.GET_COUNT(ctypes.c_char_p(i[0])))
      print "Decresed count status is",g.value,"and value is",oo.value
      if oo.value == 0:
        m_checksum = sql.exeq('select m_checksum from log where m_checksum="%s"'%(names[int(no)-1][1]))
        if m_checksum == 0:
          sql.exeq('delete from 256kb_chunks where m_checksum="%s"')
          sql.exeq('commit')
        ree = sql.exeq('select * from 256kb_chunks where c_checksum="%s" and m_checksum="%s"'%(i[0],names[int(no)-1][1]))
        print "deleting",ree
        sql.exeq('delete from 256kb_chunks where c_checksum="%s" and m_checksum="%s"'%(i[0],names[int(no)-1][1]))
        sql.exeq('commit')
        ree = sql.exeq('select * from 256kb_chunks where c_checksum="%s" and m_checksum="%s"'%(i[0],names[int(no)-1][1]))
        print "After deletion",ree
    m1_checksum = sql.exeq('select m_checksum from log where m_checksum="%s"'%(names[int(no)-1][1]))
    if m1_checksum == 0:
      sql.exeq('delete from 256kb_chunks where m_checksum="%s"'%(names[int(no)-1][1]))
      sql.exeq('commit')    
        
    #sql.cursor.execute('select * from log where username="%s" and m_checksum="%s"'%(client["username"], names[int(no)-1][1]))
    sql.exeq('commit')
    print "Ended deletion..."
  return
