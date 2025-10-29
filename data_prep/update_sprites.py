"""
Update sprite URLs for existing Pokemon in the database.
"""

import requests
import sqlite3
import time

conn = sqlite3.connect("pkmn_battle_station.db")
cursor = conn.cursor()

# Get all Pokemon without sprite URLs
cursor.execute(
    "SELECT id, name FROM pokemon_fact WHERE sprite_url IS NULL OR sprite_url = ''"
)
pokemon_list = cursor.fetchall()

print(f"Updating sprite URLs for {len(pokemon_list)} Pokemon...")

for idx, (poke_id, poke_name) in enumerate(pokemon_list, 1):
    try:
        # Fetch from PokeAPI
        url = f"https://pokeapi.co/api/v2/pokemon/{poke_id}"
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()
        sprite_url = data.get("sprites", {}).get("front_default", None)

        # Update database
        cursor.execute(
            "UPDATE pokemon_fact SET sprite_url = ? WHERE id = ?", (sprite_url, poke_id)
        )

        if idx % 50 == 0:
            print(f"Processed {idx}/{len(pokemon_list)}...")
            conn.commit()

        # Rate limiting
        time.sleep(0.1)

    except Exception as e:
        print(f"Error updating {poke_name}: {e}")
        continue

conn.commit()
conn.close()
print(f"\nCompleted! Updated {len(pokemon_list)} Pokemon sprite URLs.")
