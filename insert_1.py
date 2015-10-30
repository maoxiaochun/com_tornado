import sqlite3

conn = sqlite3.connect('test.db')
print "Opened database successfully";

conn.execute("INSERT INTO authors (NAME,PASSWD) \
      VALUES ('Paul_10', '32California')");

conn.execute("INSERT INTO authors (NAME,PASSWD) \
      VALUES ('Allen_10', '25Texas')");

conn.execute("INSERT INTO authors (NAME,PASSWD) \
      VALUES ('Teddy_10', '23Norway' )");

conn.execute("INSERT INTO authors (NAME,PASSWD) \
      VALUES ('Mark_10', '25Rich-Mond')");

conn.execute("INSERT INTO authors (NAME,PASSWD) \
      VALUES ('Paul_12', '32California')");

conn.execute("INSERT INTO authors (NAME,PASSWD) \
      VALUES ('Allen_12', '25Texas')");

conn.execute("INSERT INTO authors (NAME,PASSWD) \
      VALUES ('Teddy_12', '23Norway' )");

conn.execute("INSERT INTO authors (NAME,PASSWD) \
      VALUES ('Mark_12', '25Rich-Mond')");
conn.execute("INSERT INTO authors (NAME,PASSWD) \
      VALUES ('Paul_13', '32California')");

conn.execute("INSERT INTO authors (NAME,PASSWD) \
      VALUES ('Allen_13', '25Texas')");

conn.execute("INSERT INTO authors (NAME,PASSWD) \
      VALUES ('Teddy_13', '23Norway' )");

conn.execute("INSERT INTO authors (NAME,PASSWD) \
      VALUES ('Mark_13', '25Rich-Mond')");
conn.execute("INSERT INTO authors (NAME,PASSWD) \
      VALUES ('Paul_14', '32California')");

conn.execute("INSERT INTO authors (NAME,PASSWD) \
      VALUES ('Allen_14', '25Texas')");

conn.execute("INSERT INTO authors (NAME,PASSWD) \
      VALUES ('Teddy_14', '23Norway' )");

conn.execute("INSERT INTO authors (NAME,PASSWD) \
      VALUES ('Mark_14', '25Rich-Mond')");
conn.execute("INSERT INTO authors (NAME,PASSWD) \
      VALUES ('Paul_15', '32California')");

conn.execute("INSERT INTO authors (NAME,PASSWD) \
      VALUES ('Allen_15', '25Texas')");

conn.execute("INSERT INTO authors (NAME,PASSWD) \
      VALUES ('Teddy_15', '23Norway' )");

conn.execute("INSERT INTO authors (NAME,PASSWD) \
      VALUES ('Mark_15', '25Rich-Mond')");



conn.commit()
print "Records created successfully";
conn.close()
