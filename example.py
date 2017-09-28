import sqlite3
import time

conn = sqlite3.connect('SpiderDB.db')
c = conn.cursor()
cursor = c.execute("select IPaddress, port, writeTime from proxyServer order by writeTime DESC")
rl = cursor.fetchall()
proxyServerList = []
for row in rl:
    proxyServerList.append("%s:%s" % (row[0], row[1]))

print(len(proxyServerList))
