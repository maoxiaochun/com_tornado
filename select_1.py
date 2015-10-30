#!/usr/bin/python

import sqlite3

conn = sqlite3.connect('test.db')
print "Opened database successfully";
cur = conn.cursor()
cursor = cur.execute("SELECT  name, passwd from authors")
lst = cursor.fetchall()
for i in lst:
   print 'name:',i[0]

if 'Paul1' in (i for i,j in lst):
   print 'woca'
print "Operation done successfully";
print len(lst)
conn.close()
