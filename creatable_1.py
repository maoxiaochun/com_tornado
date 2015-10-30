import sqlite3

conn = sqlite3.connect('test.db')
print "Opened database successfully";

conn.execute('''CREATE TABLE authors
       (
       NAME           TEXT  PRIMARY KEY  NOT NULL,
       PASSWD         TEXT     NOT NULL);''')
print "Table created successfully";

conn.close()
