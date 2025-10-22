import requests
import sqlite3

# Create or connect to the SQLite database
connection = sqlite3.connect("pkmn_battle_station.db")
cursor = connection.cursor()

# Fetch the list of all moves from PokeAPI
response = requests.get("https://pokeapi.co/api/v2/move?limit=937")
data = response.json()
moves_list = data["results"]

print(f"Fetching {len(moves_list)} moves from PokeAPI...")

for idx, move in enumerate(moves_list, 1):
    url = move["url"]

    try:
        move_data = requests.get(url).json()

        # Extract move details
        move_name = move_data["name"]
        power = move_data.get("power")  # Can be None for status moves
        accuracy = move_data.get("accuracy")  # Can be None for some moves
        pp = move_data.get("pp", 0)
        move_type = move_data["type"]["name"] if move_data.get("type") else None
        damage_class = (
            move_data["damage_class"]["name"] if move_data.get("damage_class") else None
        )
        priority = move_data.get("priority", 0)

        # Insert data into the database
        cursor.execute(
            """
            INSERT OR REPLACE INTO moves_dim (
                name, power, accuracy, pp, type, damage_class, priority
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (move_name, power, accuracy, pp, move_type, damage_class, priority),
        )

        # Print progress every 100 moves
        if idx % 100 == 0:
            print(f"Processed {idx}/{len(moves_list)} moves...")
            connection.commit()  # Commit periodically

    except Exception as e:
        print(f"Error processing move {move['name']}: {e}")
        continue

# Final commit and close
connection.commit()
print(f"\nSuccessfully cached {len(moves_list)} moves in the database!")
connection.close()
