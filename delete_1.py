#!/usr/bin/python

import sqlite3

conn = sqlite3.connect('test.db')
print "Opened database successfully";

conn.execute("DELETE from COMPANY where salary<6200000;")
conn.commit
print "Total number of rows deleted :", conn.total_changes


conn.commit()
print "Operation done successfully";
conn.close()
