"""
Pokemon Details Page - Detailed view of a single Pokemon
"""

import streamlit as st
import sqlite3

st.set_page_config(page_title="Pokemon Details", page_icon="📋", layout="wide")

# Get pokemon name from query params
query_params = st.query_params
pokemon_name = query_params.get("pokemon", None)

if not pokemon_name:
    st.error("No Pokemon specified!")
    st.info("Please select a Pokemon from the Pokedex.")
    st.stop()

# Connect to database
conn = sqlite3.connect("data_prep/pkmn_battle_station.db")
cursor = conn.cursor()

# Get Pokemon data
cursor.execute(
    """
    SELECT id, name, hp, attack, defense, special_attack, special_defense, speed,
           type1, type2, sprite_url
    FROM pokemon_fact
    WHERE name = ?
    """,
    (pokemon_name,),
)
pokemon_data = cursor.fetchone()

if not pokemon_data:
    st.error(f"Pokemon '{pokemon_name}' not found!")
    conn.close()
    st.stop()

(
    poke_id,
    name,
    hp,
    attack,
    defense,
    sp_atk,
    sp_def,
    speed,
    type1,
    type2,
    sprite_url,
) = pokemon_data

# Get Smogon set if available
cursor.execute(
    """
    SELECT ability, item, nature, move1, move2, move3, move4,
           ev_hp, ev_attack, ev_defense, ev_special_attack, ev_special_defense, ev_speed,
           tier
    FROM smogon_sets
    WHERE pokemon_name = ?
    """,
    (pokemon_name,),
)
smogon_data = cursor.fetchone()

conn.close()

# Header with image and basic info
col1, col2 = st.columns([1, 2])

with col1:
    if sprite_url:
        st.image(sprite_url, width=200)
    else:
        st.info("No image available")

with col2:
    st.title(f"#{poke_id:03d} {name.title()}")

    # Types
    type_str = f"**Type:** {type1.title()}"
    if type2:
        type_str += f" / {type2.title()}"
    st.markdown(type_str)

    if smogon_data:
        tier = smogon_data[12]
        st.markdown(f"**Tier:** {tier}")

st.markdown("---")

# Base Stats
st.header("📊 Base Stats")

total_stats = hp + attack + defense + sp_atk + sp_def + speed

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("HP", hp)
    st.metric("Attack", attack)

with col2:
    st.metric("Defense", defense)
    st.metric("Sp. Attack", sp_atk)

with col3:
    st.metric("Sp. Defense", sp_def)
    st.metric("Speed", speed)

st.markdown(f"### Total: **{total_stats}**")

# Visual stat bars
st.subheader("Stat Distribution")
st.progress(hp / 255, text=f"HP: {hp}")
st.progress(attack / 255, text=f"Attack: {attack}")
st.progress(defense / 255, text=f"Defense: {defense}")
st.progress(sp_atk / 255, text=f"Special Attack: {sp_atk}")
st.progress(sp_def / 255, text=f"Special Defense: {sp_def}")
st.progress(speed / 255, text=f"Speed: {speed}")

st.markdown("---")

# Competitive Moveset
st.header("⚔️ Competitive Moveset")

if smogon_data:
    (
        ability,
        item,
        nature,
        move1,
        move2,
        move3,
        move4,
        ev_hp,
        ev_atk,
        ev_def,
        ev_spatk,
        ev_spdef,
        ev_spd,
        tier,
    ) = smogon_data

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Build")
        st.write(f"**Ability:** {ability.title() if ability else 'Unknown'}")
        st.write(f"**Item:** {item.replace('-', ' ').title() if item else 'None'}")
        st.write(f"**Nature:** {nature.title() if nature else 'Hardy'}")

        st.subheader("Moves")
        moves = [move1, move2, move3, move4]
        for i, move in enumerate(moves, 1):
            if move:
                st.write(f"{i}. {move.replace('-', ' ').title()}")
            else:
                st.write(f"{i}. (Empty)")

    with col2:
        st.subheader("EV Spread")
        evs = {
            "HP": ev_hp or 0,
            "Attack": ev_atk or 0,
            "Defense": ev_def or 0,
            "Sp. Attack": ev_spatk or 0,
            "Sp. Defense": ev_spdef or 0,
            "Speed": ev_spd or 0,
        }

        total_evs = sum(evs.values())

        for stat_name, ev_value in evs.items():
            if ev_value > 0:
                st.write(f"**{stat_name}:** {ev_value}")

        st.write(f"\n**Total EVs:** {total_evs} / 510")
else:
    st.info("No competitive moveset available for this Pokemon.")
    st.markdown(
        "This Pokemon may not have Smogon data yet. Check back after running the Smogon scraper!"
    )

st.markdown("---")

# Action buttons
col1, col2 = st.columns(2)

with col1:
    if st.button("⬅️ Back to Pokedex", use_container_width=True):
        st.switch_page("pages/1_Pokedex.py")

with col2:
    if st.button("⚔️ Battle with this Pokemon", use_container_width=True):
        st.switch_page("pages/2_Battle_Simulator.py")
