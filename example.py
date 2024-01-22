import sqlite3


# Establish a connection and a cursor
connection = sqlite3.connect("events.db")
cursor = connection.cursor()

# cursor serves as an object that can execute SQL queries
# Querry the data
cursor.execute("Select * From events WHERE date='2088.10.15'")
row = cursor.fetchall()
print(row)

# Insert Data
new_rows = [('Hens', 'Hen City', '2088.10.16'), ('Cats', 'Cat City', '2088.10.17')]
cursor.executemany("INSERT INTO events VALUES(?,?,?)", new_rows)
connection.commit()