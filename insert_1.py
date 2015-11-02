import sqlite3

conn = sqlite3.connect('test.db')
print "Opened database successfully";

for i in range(1,30):
    conn.execute("INSERT INTO authors (NAME,PASSWD)"
      "VALUES ('test_%s', '32djujiij')"%(i));





conn.commit()
print "Records created successfully";
conn.close()
