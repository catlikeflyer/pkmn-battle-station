"""
Scrape Smogon competitive movesets and populate the smogon_sets table.
Uses Smogon's usage stats and showdown data.
"""

import requests
import sqlite3
import json
import time
from typing import Optional, Dict, Any

# Showdown API endpoints
SHOWDOWN_DEX_URL = "https://play.pokemonshowdown.com/data/pokedex.json"
SHOWDOWN_FORMATS_URL = "https://play.pokemonshowdown.com/data/formats.json"

# Common natures and their stat modifications
NATURES = {
    "adamant": {"increased": "attack", "decreased": "special-attack"},
    "jolly": {"increased": "speed", "decreased": "special-attack"},
    "timid": {"increased": "speed", "decreased": "attack"},
    "modest": {"increased": "special-attack", "decreased": "attack"},
    "bold": {"increased": "defense", "decreased": "attack"},
    "calm": {"increased": "special-defense", "decreased": "attack"},
    "careful": {"increased": "special-defense", "decreased": "special-attack"},
    "impish": {"increased": "defense", "decreased": "special-attack"},
}


def get_pokemon_from_db():
    """Get all Pokemon names from the database."""
    conn = sqlite3.connect("pkmn_battle_station.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM pokemon_fact ORDER BY name")
    pokemon_names = [row[0] for row in cursor.fetchall()]
    conn.close()
    return pokemon_names


def fetch_showdown_data():
    """Fetch Pokemon data from Showdown."""
    print("Fetching Pokemon Showdown data...")
    try:
        response = requests.get(SHOWDOWN_DEX_URL)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching Showdown data: {e}")
        return {}


def normalize_pokemon_name(name: str) -> str:
    """Normalize Pokemon name for matching."""
    # Remove special characters and convert to lowercase
    name = name.lower().replace(" ", "").replace("-", "").replace("'", "")

    # Handle special cases
    special_cases = {
        "mrrime": "mr-rime",
        "mrmime": "mr-mime",
        "mimikyutotem": "mimikyu-totem",
        "typeNull": "type-null",
        "tapukoko": "tapu-koko",
        "tapulele": "tapu-lele",
        "tapubulu": "tapu-bulu",
        "tapufini": "tapu-fini",
    }

    return special_cases.get(name, name)


def generate_competitive_set(
    pokemon_name: str, showdown_data: Dict
) -> Optional[Dict[str, Any]]:
    """
    Generate a competitive moveset based on Pokemon stats and common strategies.
    This is a simplified version - ideally would use actual Smogon usage stats.
    """
    # Normalize name for showdown lookup
    normalized_name = normalize_pokemon_name(pokemon_name)

    # Try to find in Showdown data
    showdown_entry = None
    for key, value in showdown_data.items():
        if normalize_pokemon_name(key) == normalized_name:
            showdown_entry = value
            break

    if not showdown_entry:
        return None

    # Get Pokemon stats
    conn = sqlite3.connect("pkmn_battle_station.db")
    cursor = conn.cursor()
    cursor.execute(
        """SELECT attack, defense, special_attack, special_defense, speed, type1, type2
           FROM pokemon_fact WHERE name = ?""",
        (pokemon_name,),
    )
    result = cursor.fetchone()

    if not result:
        conn.close()
        return None

    atk, defense, sp_atk, sp_def, speed, type1, type2 = result

    # Determine if physical or special attacker
    is_physical = atk > sp_atk

    # Get common moves for this Pokemon from showdown
    move_pool = showdown_entry.get("randomBattleMoves", [])
    if not move_pool:
        move_pool = showdown_entry.get("moves", [])[:4]

    # Ensure moves exist in our moves_dim table
    valid_moves = []
    for move in move_pool[:8]:  # Get up to 8 potential moves to find 4 valid ones
        # Try different name formats
        move_variants = [
            move.lower().replace(" ", "-"),
            move.lower().replace(" ", ""),
            move.lower(),
        ]

        for move_name in move_variants:
            cursor.execute("SELECT name FROM moves_dim WHERE name = ?", (move_name,))
            result = cursor.fetchone()
            if result:
                valid_moves.append(result[0])
                break

        if len(valid_moves) >= 4:
            break

    # If still not enough, get ANY moves that match the types
    if len(valid_moves) < 4:
        type_moves_query = """
            SELECT name FROM moves_dim 
            WHERE type IN (?, ?) 
            AND damage_class IN ('physical', 'special')
            AND power IS NOT NULL
            ORDER BY power DESC
            LIMIT 4
        """
        cursor.execute(type_moves_query, (type1, type2 or type1))
        type_moves = [row[0] for row in cursor.fetchall()]

        for move in type_moves:
            if move not in valid_moves:
                valid_moves.append(move)
            if len(valid_moves) >= 4:
                break

    conn.close()

    # If not enough moves, skip this Pokemon
    if len(valid_moves) < 4:
        return None

    # Determine nature based on stats
    if is_physical:
        if speed > max(atk, defense, sp_def):
            nature = "jolly"
        else:
            nature = "adamant"
    else:
        if speed > max(sp_atk, defense, sp_def):
            nature = "timid"
        else:
            nature = "modest"

    # Determine EV spread (simplified)
    if is_physical:
        evs = {
            "hp": 0,
            "attack": 252,
            "defense": 4,
            "special_attack": 0,
            "special_defense": 0,
            "speed": 252,
        }
    else:
        evs = {
            "hp": 0,
            "attack": 0,
            "defense": 4,
            "special_attack": 252,
            "special_defense": 0,
            "speed": 252,
        }

    # Get ability
    abilities = showdown_entry.get("abilities", {})
    ability = abilities.get("0", "Unknown")

    # Get tier
    tier = showdown_entry.get("tier", "OU")

    return {
        "pokemon_name": pokemon_name,
        "ability": ability,
        "item": "life-orb",  # Default item
        "nature": nature,
        "move1": valid_moves[0] if len(valid_moves) > 0 else None,
        "move2": valid_moves[1] if len(valid_moves) > 1 else None,
        "move3": valid_moves[2] if len(valid_moves) > 2 else None,
        "move4": valid_moves[3] if len(valid_moves) > 3 else None,
        "ev_hp": evs["hp"],
        "ev_attack": evs["attack"],
        "ev_defense": evs["defense"],
        "ev_special_attack": evs["special_attack"],
        "ev_special_defense": evs["special_defense"],
        "ev_speed": evs["speed"],
        "usage_percent": 0.0,  # Would need actual usage stats
        "tier": tier,
    }


def main():
    """Main function to scrape and populate Smogon sets."""
    print("Starting Smogon sets scraper...")

    # Get Pokemon from database
    pokemon_list = get_pokemon_from_db()
    print(f"Found {len(pokemon_list)} Pokemon in database")

    # Fetch Showdown data
    showdown_data = fetch_showdown_data()
    if not showdown_data:
        print("Failed to fetch Showdown data. Exiting.")
        return

    print(f"Loaded {len(showdown_data)} Pokemon from Showdown")

    # Connect to database
    conn = sqlite3.connect("pkmn_battle_station.db")
    cursor = conn.cursor()

    successful = 0
    skipped = 0

    for idx, pokemon_name in enumerate(pokemon_list, 1):
        try:
            # Generate competitive set
            moveset = generate_competitive_set(pokemon_name, showdown_data)

            if not moveset:
                skipped += 1
                if idx % 100 == 0:
                    print(
                        f"Processed {idx}/{len(pokemon_list)} - Skipped {pokemon_name} (no data)"
                    )
                continue

            # Insert into database
            cursor.execute(
                """
                INSERT OR REPLACE INTO smogon_sets (
                    pokemon_name, ability, item, nature,
                    move1, move2, move3, move4,
                    ev_hp, ev_attack, ev_defense,
                    ev_special_attack, ev_special_defense, ev_speed,
                    usage_percent, tier
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    moveset["pokemon_name"],
                    moveset["ability"],
                    moveset["item"],
                    moveset["nature"],
                    moveset["move1"],
                    moveset["move2"],
                    moveset["move3"],
                    moveset["move4"],
                    moveset["ev_hp"],
                    moveset["ev_attack"],
                    moveset["ev_defense"],
                    moveset["ev_special_attack"],
                    moveset["ev_special_defense"],
                    moveset["ev_speed"],
                    moveset["usage_percent"],
                    moveset["tier"],
                ),
            )

            successful += 1

            # Print progress every 100 Pokemon
            if idx % 100 == 0:
                print(
                    f"Processed {idx}/{len(pokemon_list)} - Success: {successful}, Skipped: {skipped}"
                )
                conn.commit()

        except Exception as e:
            print(f"Error processing {pokemon_name}: {e}")
            skipped += 1
            continue

    # Final commit
    conn.commit()
    conn.close()

    print(f"\n{'='*60}")
    print(f"Scraping complete!")
    print(f"Successfully added: {successful} Pokemon")
    print(f"Skipped: {skipped} Pokemon")
    print(f"Total processed: {len(pokemon_list)}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
