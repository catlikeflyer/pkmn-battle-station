"""
Pokedex Page - Browse and explore all Pokemon
"""

import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="Pokedex", page_icon="📖", layout="wide")

st.title("📖 Pokedex")
st.markdown("Browse and explore all Pokemon in the database")

# Connect to database
conn = sqlite3.connect("data_prep/pkmn_battle_station.db")

# Get Pokemon data
query = """
SELECT 
    id,
    name,
    type1,
    type2,
    hp,
    attack,
    defense,
    special_attack,
    special_defense,
    speed,
    (hp + attack + defense + special_attack + special_defense + speed) as total
FROM pokemon_fact
ORDER BY id
"""

df = pd.read_sql_query(query, conn)
conn.close()

if df.empty:
    st.error(
        "No Pokemon found in database. Please run `python data_prep/pokemon_fact.py` first."
    )
    st.stop()

# Sidebar filters
st.sidebar.header("🔍 Filters")

# Type filter
all_types = set(df["type1"].tolist() + df["type2"].dropna().tolist())
all_types = sorted([t for t in all_types if t])
selected_types = st.sidebar.multiselect("Filter by Type", all_types)

# Stat range filters
st.sidebar.subheader("Stat Ranges")
min_total = st.sidebar.slider("Minimum Total Stats", 0, 800, 0)
max_total = st.sidebar.slider("Maximum Total Stats", 0, 800, 800)

# Search by name
search_query = st.sidebar.text_input("🔎 Search by name", "")

# Apply filters
filtered_df = df.copy()

if selected_types:
    filtered_df = filtered_df[
        filtered_df["type1"].isin(selected_types)
        | filtered_df["type2"].isin(selected_types)
    ]

filtered_df = filtered_df[
    (filtered_df["total"] >= min_total) & (filtered_df["total"] <= max_total)
]

if search_query:
    filtered_df = filtered_df[
        filtered_df["name"].str.contains(search_query.lower(), case=False)
    ]

# Sort options
sort_by = st.sidebar.selectbox(
    "Sort by",
    [
        "ID",
        "Name",
        "Total Stats",
        "HP",
        "Attack",
        "Defense",
        "Sp. Attack",
        "Sp. Defense",
        "Speed",
    ],
)

sort_mapping = {
    "ID": "id",
    "Name": "name",
    "Total Stats": "total",
    "HP": "hp",
    "Attack": "attack",
    "Defense": "defense",
    "Sp. Attack": "special_attack",
    "Sp. Defense": "special_defense",
    "Speed": "speed",
}

sort_order = st.sidebar.radio("Order", ["Ascending", "Descending"])
filtered_df = filtered_df.sort_values(
    by=sort_mapping[sort_by], ascending=(sort_order == "Ascending")
)

# Display stats
st.markdown(f"### Showing {len(filtered_df)} of {len(df)} Pokemon")

# Display mode
display_mode = st.radio("Display Mode", ["Cards", "Table"], horizontal=True)

if display_mode == "Cards":
    # Card view
    cols_per_row = 3
    rows = len(filtered_df) // cols_per_row + (
        1 if len(filtered_df) % cols_per_row else 0
    )

    for row in range(rows):
        cols = st.columns(cols_per_row)
        for col_idx in range(cols_per_row):
            idx = row * cols_per_row + col_idx
            if idx < len(filtered_df):
                pokemon = filtered_df.iloc[idx]

                with cols[col_idx]:
                    with st.container(border=True):
                        # Pokemon name and ID
                        st.markdown(
                            f"### #{pokemon['id']:03d} {pokemon['name'].title()}"
                        )

                        # Types
                        type_str = f"**Type:** {pokemon['type1'].title()}"
                        if pd.notna(pokemon["type2"]):
                            type_str += f" / {pokemon['type2'].title()}"
                        st.markdown(type_str)

                        # Stats
                        st.markdown("**Base Stats:**")
                        st.progress(pokemon["hp"] / 255, text=f"HP: {pokemon['hp']}")
                        st.progress(
                            pokemon["attack"] / 255, text=f"Attack: {pokemon['attack']}"
                        )
                        st.progress(
                            pokemon["defense"] / 255,
                            text=f"Defense: {pokemon['defense']}",
                        )
                        st.progress(
                            pokemon["special_attack"] / 255,
                            text=f"Sp. Atk: {pokemon['special_attack']}",
                        )
                        st.progress(
                            pokemon["special_defense"] / 255,
                            text=f"Sp. Def: {pokemon['special_defense']}",
                        )
                        st.progress(
                            pokemon["speed"] / 255, text=f"Speed: {pokemon['speed']}"
                        )

                        # Total
                        st.metric("Total", int(pokemon["total"]))

else:
    # Table view
    display_df = filtered_df.copy()
    display_df["name"] = display_df["name"].str.title()
    display_df["type1"] = display_df["type1"].str.title()
    display_df["type2"] = display_df["type2"].str.title()

    # Rename columns for display
    display_df = display_df.rename(
        columns={
            "id": "ID",
            "name": "Name",
            "type1": "Type 1",
            "type2": "Type 2",
            "hp": "HP",
            "attack": "Attack",
            "defense": "Defense",
            "special_attack": "Sp. Attack",
            "special_defense": "Sp. Defense",
            "speed": "Speed",
            "total": "Total",
        }
    )

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "ID": st.column_config.NumberColumn(format="%03d"),
            "HP": st.column_config.ProgressColumn(
                min_value=0,
                max_value=255,
            ),
            "Attack": st.column_config.ProgressColumn(
                min_value=0,
                max_value=255,
            ),
            "Defense": st.column_config.ProgressColumn(
                min_value=0,
                max_value=255,
            ),
            "Sp. Attack": st.column_config.ProgressColumn(
                min_value=0,
                max_value=255,
            ),
            "Sp. Defense": st.column_config.ProgressColumn(
                min_value=0,
                max_value=255,
            ),
            "Speed": st.column_config.ProgressColumn(
                min_value=0,
                max_value=255,
            ),
        },
    )

# Stats summary
st.markdown("---")
st.subheader("📊 Statistics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Pokemon", len(filtered_df))

with col2:
    avg_total = filtered_df["total"].mean()
    st.metric("Average Total Stats", f"{avg_total:.1f}")

with col3:
    highest = filtered_df.loc[filtered_df["total"].idxmax()]
    st.metric("Highest Total", f"{highest['name'].title()}", f"{int(highest['total'])}")

with col4:
    lowest = filtered_df.loc[filtered_df["total"].idxmin()]
    st.metric("Lowest Total", f"{lowest['name'].title()}", f"{int(lowest['total'])}")
