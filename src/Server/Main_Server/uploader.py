import chunks_manager
import net
import os
def getFileChecksum(sql, client):
  # This function will return m_checksum of file which user wants to download
  names = sql.MakeList(client)
  if names != 0:
    listt = '\n'.join(x[0] for x in names)
    client["socket"].send(listt)
    no = client["socket"].recv(10)
    print "Here is filename query...",no,names[int(no)-1][0]
    #return sql.get_m_checksum(client, names[int(no)-1][0])
    return names[int(no)-1]
  else:
    client["socket"].send('UPLOAD!')
    return 0

def uploader(sql, client, sub_servers, C_lib):
  m_checksum = getFileChecksum(sql, client)
  # Now m_checksum is an array..
  # 0th index --> actual checksum
  # 1th index --> actual filename example a.out, simple.txt
  if m_checksum != 0:
    dummy = sql.get_c_checksum(m_checksum[1])
    print "---------->",dummy,m_checksum[1]
    chunks_manager.RESTORE_ALL_256_KB(sub_servers, sql, dummy, m_checksum[1], C_lib)
    print "Restored parts!"
    #net.uploadFile(names[int(no)-1][0], client["socket"])
    net.uploadFile(m_checksum[1], client["socket"])
    os.remove(m_checksum[1])
    print "File is uploaded!"
