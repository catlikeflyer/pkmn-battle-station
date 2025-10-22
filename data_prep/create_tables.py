import sqlite3

# Create or connect to the SQLite database
connection = sqlite3.connect("pkmn_battle_station.db")
cursor = connection.cursor()

# Read and execute the SQL script to create tables
with open("./create_tables.sql", "r") as sql_file:
    sql_script = sql_file.read()

cursor.executescript(sql_script)
# Commit changes and close the connection
connection.commit()
connection.close()
