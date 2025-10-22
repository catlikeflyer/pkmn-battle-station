import requests
import sqlite3

# Create or connect to the SQLite database
connection = sqlite3.connect("pkmn_battle_station.db")
cursor = connection.cursor()


# Function to fetch data from a given URL
response = requests.get("https://pokeapi.co/api/v2/pokemon?limit=1302")
data = response.json()
pokemon_list = data["results"]
for pokemon in pokemon_list:
    url = pokemon["url"]

    pokemon_data = requests.get(url).json()
    pokemon_id = pokemon_data["id"]
    pokemon_name = pokemon_data["name"]
    # Extract types
    type1 = pokemon_data["types"][0]["type"]["name"]
    type2 = (
        pokemon_data["types"][1]["type"]["name"]
        if len(pokemon_data["types"]) > 1
        else None
    )

    # Extract base stats
    stats = {stat["stat"]["name"]: stat["base_stat"] for stat in pokemon_data["stats"]}
    hp = stats.get("hp", 0)
    attack = stats.get("attack", 0)
    defense = stats.get("defense", 0)
    sp_atk = stats.get("special-attack", 0)
    sp_def = stats.get("special-defense", 0)
    speed = stats.get("speed", 0)

    # Insert data into the database
    cursor.execute(
        """
        INSERT OR REPLACE INTO pokemon (
            id, name, type1, type2, hp, attack, defense, sp_at
            sp_def, speed
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            pokemon_id,
            pokemon_name,
            type1,
            type2,
            hp,
            attack,
            defense,
            sp_atk,
            sp_def,
            speed,
        ),
    )
# Commit changes and close the connection
connection.commit()
connection.close()
