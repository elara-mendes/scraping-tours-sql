import sqlite3

# Create connection
connection = sqlite3.connect('data.db')
cursor = connection.cursor()

# Query data from a specific row
cursor.execute("SELECT * FROM events WHERE date='2029-20-12'")
row = cursor.fetchall()
print(row)

# Get data from specifics columns
cursor.execute("SELECT band, date FROM events WHERE date='2028-20-12'")
row = cursor.fetchall()
print(row)

# Add data to table
# add_rows = [('Sakura', 'Konoha', '2029-20-12'), ('Sai', 'Konoha', '2028-20-12')]
# cursor.executemany("INSERT INTO events VALUES(?, ?, ?)", add_rows)
# connection.commit()

# Get all data
cursor.execute("SELECT * FROM events")
row = cursor.fetchall()
print(row)