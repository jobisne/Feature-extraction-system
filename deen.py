import sqlite3

conn = sqlite3.connect('platNum.db')
print "Opened database successfully";

conn.execute('CREATE TABLE platenumber (fileName TEXT, textExtracted TEXT, timeIn NUMERIC, timeOut NUMERIC)')
print "Table created successfully";
conn.close()

