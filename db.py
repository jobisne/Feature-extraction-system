import sqlite3

conn = sqlite3.connect('database.db')
print "Opened database successfully";

conn.execute('CREATE TABLE plate (fileName TEXT, textExtracted TEXT, timeIn NUMERIC, timeOut NUMERIC)')
print "Table created successfully";
conn.close()

