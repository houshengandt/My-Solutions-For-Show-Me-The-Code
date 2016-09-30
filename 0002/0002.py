import MySQLdb

db = MySQLdb.connect("localhost", "root", passwd="******", db="u0002")
# 填写数据库信息

cursor = db.cursor()
cursor.execute("DROP TABLE IF EXISTS U0002")    # will be a warning at the first run! :Warning: Unknown table 'u0002.u0002'
cursor.execute("CREATE TABLE U0002 (mykey VARCHAR(36))")
cursor.execute("LOAD DATA LOCAL INFILE 'key.txt' INTO TABLE u0002 LINES TERMINATED BY '\r\n';")
db.commit()
db.close()
