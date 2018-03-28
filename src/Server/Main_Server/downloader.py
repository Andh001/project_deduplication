import chunks_manager
import os
import net
import ctypes
def isFileExists(client, strr, sql, C_lib):
  # This function will check whether file is exists or not..
  # it is identified by unique m_checksum
  if sql.CheckFileChecksum(strr[0]):
    sql.Update(client, strr)
    client["socket"].send('FILE_EXISTS')
    c = sql.exeq('select c_checksum from 256kb_chunks where m_checksum ="%s"'%(strr[0]))
    for i in c:
      g = ctypes.c_int(C_lib.INC_COUNT(i[0]))
      if g.value == 1:
        print "Increased count of", i[0]
      else:
        print "Failed to increase count of",i[0]
    return False
  else:
    client["socket"].send('NOT_EXISTS')
    return True

def downloader(sql, client, socks, C_lib):
  strr = client["socket"].recv(1024)
  while strr != 'STOP_UPLOAD':
    strr = strr.split('*')
    filename = strr[1] # actual filename, a.txt, 3.pdf etc...
    m_checksum = strr[0] # file content checksum
    status = isFileExists(client, strr, sql, C_lib)
    if status:
      net.downloadFile(m_checksum, client["socket"])
      # chane filename --> m_checksum
      print "File",filename,"is received and saved on Main Server as",m_checksum
      #names_arr = Chunk._256_kb_split(filename)   
      chunks_manager.STORE_ALL_256_KB_001(socks, sql, m_checksum, C_lib)
      os.remove(m_checksum)
      sql._insert_(['username','filename','m_checksum'], [client["username"],strr[1],strr[0]], 'log')
    strr = client["socket"].recv(1024)
    print "Client's next query is",strr

