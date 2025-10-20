import requests
import sqlite3

# Create or connect to the SQLite database
connection = sqlite3.connect('pkmn_battle_station.db')
cursor = connection.cursor()

# Read and execute the SQL script to create tables
with open('sql/create_tables.sql', 'r') as sql_file:
    sql_script = sql_file.read()

cursor.executescript(sql_script)

# Function to fetch data from a given URL
response = requests.get("https://pokeapi.co/api/v2/pokemon?limit=1302")
data = response.json()




