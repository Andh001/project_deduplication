import MySQLdb
# Every executed query returnes No. of rows
# rows can be displayed with "print cursor.fetchall()" after execution
class SQL:
	def __init__(self):
		self.Connection = MySQLdb.connect("localhost", "root", "root", "log")
		self.cursor = self.Connection.cursor()

	def exeq(self, query):
		if self.cursor.execute(query):
			#self.cursor.execute("commit")
			return self.cursor.fetchall()
		else:
			print "??????"
			return 0

	def get_m_checksum(self,client,filename):
		return self.exeq('select m_checksum from log where username="%s" and filename="%s"' %(client["username"], filename))

	def get_c_checksum(self, m_checksum):
		return self.exeq('select c_checksum from 256kb_chunks where m_checksum="%s" order by seq_no'%(m_checksum))

	def getCursor(self):
		self.cursor = self.Connection.cursor()
		return self.cursor

	def CheckFileName(self, filename):
		#This returnes No. of rows executed by the query
		return self.cursor.execute('select filename from log where filename = "'+filename+'"')

	def MakeList(self, client):
		return self.exeq('select filename, m_checksum from log where username="%s"'%(client["username"]))

	def Update(self, client, strr):
		# checking whether a file is uploaded by user before?
		print strr
		a = self.cursor.execute('select filename from log where m_checksum = "%s" and username = "%s"' % (strr[0], client["username"]))
		if a == 0:
			# if there is no file uploaded by any user before
			self.cursor.execute('insert into log(filename, m_checksum, username) values("'+strr[1]+'","'+strr[0]+'","'+client["username"]+'")')
		self.cursor.execute('commit')

	def CheckFileChecksum(self, checksum):
		#This returnes No. of rows executed by the query
		print "@SQL.py 42"
		return self.exeq('select m_checksum from log where m_checksum="'+checksum+'"')

	

	def _insert_(self, cols, vals, table):
		# this function creates query to insert into "table"
		# cols having columns
		# vals having values of columns
		# length of cols and vals should be same

		col = ', '.join(x for x in cols)
		val = '"'+'", "'.join(x for x in vals)+'"'
		q = "insert into "+table+"("+col+") values("+val+")"
		#return q
		self.cursor.execute(q)
		self.cursor.execute('commit')

	def _update_chunks(self, checksum, arr):
		for i in range(len(arr)):
			self._insert_(['chunk', 'checksum'], [checksum+'_'+str(i), arr[i]], 'erasure')

'''
mysql> desc log;
create table log ( checksum varchar(40), filename varchar(100), dedup varchar(100), username varchar(100), count int(11));
+----------+--------------+------+-----+---------+-------+
| Field    | Type         | Null | Key | Default | Extra |
+----------+--------------+------+-----+---------+-------+
| checksum | varchar(40)  | YES  |     | NULL    |       |
| filename | varchar(100) | YES  |     | NULL    |       |
| filesize | int(11)      | YES  |     | NULL    |       |
| dedup    | varchar(100) | YES  |     | NULL    |       |
| username | varchar(100) | YES  |     | NULL    |       |
| count    | int(11)      | YES  |     | NULL    |       |
+----------+--------------+------+-----+---------+-------+
6 rows in set (0.00 sec)

mysql> desc erasure;
create table erasure ( chunk varchar(150), checksum varchar(100));
+----------+--------------+------+-----+---------+-------+
| Field    | Type         | Null | Key | Default | Extra |
+----------+--------------+------+-----+---------+-------+
| chunk    | varchar(150) | YES  |     | NULL    |       |
| checksum | varchar(100) | YES  |     | NULL    |       |
+----------+--------------+------+-----+---------+-------+
'''
