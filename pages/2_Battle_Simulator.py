"""
Interactive Battle Simulator Page
Watch two Pokemon fight in real-time!
"""

import streamlit as st
import sqlite3
from core.pokemon import Pokemon
from core.battle import Battle

st.set_page_config(page_title="Battle Simulator", page_icon="⚔️", layout="wide")

st.title("⚔️ Battle Simulator")
st.markdown("Select two Pokemon and watch them battle!")

# Get list of Pokemon
conn = sqlite3.connect("pkmn_battle_station.db")
cursor = conn.cursor()
cursor.execute("SELECT name FROM pokemon_fact ORDER BY name")
pokemon_names = [row[0] for row in cursor.fetchall()]
conn.close()

if not pokemon_names:
    st.error("No Pokemon found in database. Please run data preparation scripts.")
    st.stop()

# Pokemon selection
col1, col2 = st.columns(2)

with col1:
    st.subheader("🔴 Pokemon 1")
    pokemon1_name = st.selectbox("Select Pokemon 1", pokemon_names, key="p1")

with col2:
    st.subheader("🔵 Pokemon 2")
    # Default to second Pokemon in list
    default_idx = min(1, len(pokemon_names) - 1)
    pokemon2_name = st.selectbox(
        "Select Pokemon 2", pokemon_names, index=default_idx, key="p2"
    )

# Battle button
if st.button("⚔️ Start Battle!", type="primary", use_container_width=True):
    if pokemon1_name == pokemon2_name:
        st.warning("Please select two different Pokemon!")
    else:
        with st.spinner("Loading Pokemon data..."):
            try:
                # Load Pokemon
                pokemon1 = Pokemon(pokemon1_name)
                pokemon2 = Pokemon(pokemon2_name)

                # Display Pokemon stats before battle
                col1, col2 = st.columns(2)

                with col1:
                    st.markdown(f"### 🔴 {pokemon1.name.title()}")
                    st.write(
                        f"**Type:** {pokemon1.type1.title()}"
                        + (f" / {pokemon1.type2.title()}" if pokemon1.type2 else "")
                    )
                    st.write(f"**HP:** {pokemon1.max_hp}")
                    st.write(f"**Attack:** {pokemon1.attack}")
                    st.write(f"**Defense:** {pokemon1.defense}")
                    st.write(f"**Sp. Atk:** {pokemon1.special_attack}")
                    st.write(f"**Sp. Def:** {pokemon1.special_defense}")
                    st.write(f"**Speed:** {pokemon1.speed}")

                    if pokemon1.moves:
                        st.write("**Moves:**")
                        for move in pokemon1.moves:
                            st.write(f"  - {move.name.title()}")

                with col2:
                    st.markdown(f"### 🔵 {pokemon2.name.title()}")
                    st.write(
                        f"**Type:** {pokemon2.type1.title()}"
                        + (f" / {pokemon2.type2.title()}" if pokemon2.type2 else "")
                    )
                    st.write(f"**HP:** {pokemon2.max_hp}")
                    st.write(f"**Attack:** {pokemon2.attack}")
                    st.write(f"**Defense:** {pokemon2.defense}")
                    st.write(f"**Sp. Atk:** {pokemon2.special_attack}")
                    st.write(f"**Sp. Def:** {pokemon2.special_defense}")
                    st.write(f"**Speed:** {pokemon2.speed}")

                    if pokemon2.moves:
                        st.write("**Moves:**")
                        for move in pokemon2.moves:
                            st.write(f"  - {move.name.title()}")

                st.markdown("---")

                # Run battle
                with st.spinner("Battle in progress..."):
                    battle = Battle(pokemon1, pokemon2)
                    winner, battle_log = battle.simulate()

                # Display battle results
                st.success(f"Battle Complete in {battle.turn} turns!")

                if winner:
                    st.balloons()
                    st.markdown(f"## 🏆 Winner: {winner.name.title()}!")
                    st.metric(
                        "Final HP",
                        f"{winner.current_hp}/{winner.max_hp}",
                        f"{winner.hp_percentage():.1f}%",
                    )
                else:
                    st.info("Battle ended in a draw!")

                # Battle log
                st.markdown("---")
                st.subheader("📜 Battle Log")

                log_container = st.container()
                with log_container:
                    for line in battle_log:
                        st.text(line)

            except Exception as e:
                st.error(f"Error during battle: {e}")
                st.exception(e)

st.markdown("---")
st.info(
    "💡 **Tip:** Battles use real Pokemon mechanics including type effectiveness, STAB, and critical hits!"
)
