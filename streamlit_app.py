"""
Pokemon Battle Station - Streamlit Dashboard
Main entry point for the interactive application.
"""

import streamlit as st
import sqlite3
from pathlib import Path

# Configure page
st.set_page_config(
    page_title="Pokemon Battle Station",
    page_icon="⚔️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown(
    """
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #FF0000 0%, #CC0000 50%, #FF0000 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding: 1rem;
    }
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
</style>
""",
    unsafe_allow_html=True,
)

# Title
st.markdown(
    '<h1 class="main-header">⚔️ Pokemon Battle Station</h1>', unsafe_allow_html=True
)
st.markdown(
    '<p class="subtitle">Determine the strongest Pokemon through battle simulations</p>',
    unsafe_allow_html=True,
)

# Check if database exists
db_path = Path("pkmn_battle_station.db")
if not db_path.exists():
    st.error("⚠️ Database not found! Please run the data preparation scripts first.")
    st.info(
        """
    **Setup Instructions:**
    1. Run `python data_prep/create_tables.py` to create database
    2. Run `python data_prep/pokemon_fact.py` to load Pokemon data
    3. Run `python data_prep/moves_dim.py` to load move data
    4. (Optional) Run script to load Smogon sets
    5. Restart this app
    """
    )
    st.stop()

# Database stats
conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

col1, col2, col3, col4 = st.columns(4)

with col1:
    cursor.execute("SELECT COUNT(*) FROM pokemon_fact")
    pokemon_count = cursor.fetchone()[0]
    st.metric("Pokemon Loaded", pokemon_count)

with col2:
    cursor.execute("SELECT COUNT(*) FROM moves_dim")
    moves_count = cursor.fetchone()[0]
    st.metric("Moves Cached", moves_count)

with col3:
    cursor.execute("SELECT COUNT(*) FROM smogon_sets")
    sets_count = cursor.fetchone()[0]
    st.metric("Smogon Sets", sets_count)

with col4:
    cursor.execute("SELECT COUNT(*) FROM battle_results")
    battles_count = cursor.fetchone()[0]
    st.metric("Battles Simulated", battles_count)

conn.close()

# Main content
st.markdown("---")

st.header("🎯 Project Overview")

col1, col2 = st.columns(2)

with col1:
    st.subheader("What This Does")
    st.write(
        """
    This project aims to answer: **"What's the strongest Pokemon?"**
    
    Through comprehensive battle simulations using:
    - ✅ Real Pokemon base stats (from PokeAPI)
    - ✅ Actual move data and damage calculations
    - 🔄 Most used competitive movesets (from Smogon)
    - 🤖 AI-driven battle strategies (NEAT algorithm)
    - 📊 ELO ranking system
    """
    )

with col2:
    st.subheader("Features")
    st.write(
        """
    **Available Pages:**
    - 🏆 **Rankings**: View top Pokemon by ELO rating
    - ⚔️ **Battle Simulator**: Watch any two Pokemon fight
    - 🏟️ **Tournament**: Run round-robin tournaments
    - 📈 **Analytics**: Deep dive into battle statistics
    - 🎨 **Type Analysis**: Type effectiveness insights
    """
    )

st.markdown("---")

# Quick actions
st.header("🚀 Quick Actions")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🎲 Random Battle", use_container_width=True):
        st.switch_page("pages/2_Battle_Simulator.py")

with col2:
    if st.button("🏆 View Rankings", use_container_width=True):
        st.switch_page("pages/1_Rankings.py")

with col3:
    if st.button("📊 Analytics Dashboard", use_container_width=True):
        st.switch_page("pages/4_Analytics.py")

st.markdown("---")

# Footer
st.markdown(
    """
<div style='text-align: center; color: #888; padding: 2rem;'>
    <p>Built with Streamlit • Data from PokeAPI & Smogon</p>
    <p>Battle simulation using authentic Pokemon mechanics</p>
</div>
""",
    unsafe_allow_html=True,
)
