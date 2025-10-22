# Pokemon Battle Station

## What's the Strongest Pokemon?

This project definitively answers that question through comprehensive battle simulations using real Pokemon mechanics, competitive movesets, and ELO rankings.

## Features

- ✅ **Complete Pokemon Data**: 900+ Pokemon with base stats from PokeAPI
- ✅ **937 Moves**: Full move database with power, accuracy, and types
- 🔄 **Smogon Movesets**: Most used competitive sets (work in progress)
- ⚔️ **Battle Simulator**: Watch Pokemon fight with authentic mechanics
- 🏆 **Rankings System**: ELO-based power rankings
- 📊 **Interactive Dashboard**: Built with Streamlit
- 🤖 **AI Strategies**: NEAT algorithm for evolved battle tactics (optional)

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Setup Database

```bash
# Navigate to data prep folder
cd data_prep

# Create database tables
python create_tables.py

# Load Pokemon data (~5 minutes)
python pokemon_fact.py

# Load move data (~10 minutes)
python moves_dim.py
```

### 3. Launch Streamlit App

```bash
# From project root
streamlit run streamlit_app.py
```

The app will open in your browser at `http://localhost:8501`

## Project Structure

```
pkmn-battle-station/
├── streamlit_app.py           # Main Streamlit app
├── requirements.txt           # Python dependencies
├── ARCHITECTURE.md            # Detailed architecture docs
│
├── data_prep/                 # Data extraction scripts
│   ├── create_tables.py       # Initialize database
│   ├── pokemon_fact.py        # Load Pokemon from PokeAPI
│   ├── moves_dim.py          # Load moves from PokeAPI
│   └── create_tables.sql      # Database schema
│
├── core/                      # Battle engine
│   ├── pokemon.py            # Pokemon class
│   ├── move.py               # Move class
│   ├── battle.py             # Battle simulator
│   └── type_chart.py         # Type effectiveness
│
├── pages/                     # Streamlit pages
│   ├── 1_Rankings.py         # View rankings
│   ├── 2_Battle_Simulator.py # Interactive battles
│   ├── 3_Tournament.py       # Run tournaments
│   ├── 4_Analytics.py        # Statistics
│   └── 5_Type_Analysis.py    # Type insights
│
└── tournament/                # Tournament system
    ├── round_robin.py        # Tournament runner
    └── elo_system.py         # ELO calculations
```

## Battle Mechanics

The simulator implements authentic Pokemon battle mechanics:

- **Damage Calculation**: Uses real Pokemon formula
- **Type Effectiveness**: Complete type chart (Gen 8+)
- **STAB Bonus**: Same Type Attack Bonus (1.5x)
- **Critical Hits**: 6.25% chance for 1.5x damage
- **Accuracy Checks**: Moves can miss based on accuracy
- **Speed Priority**: Faster Pokemon attacks first

## Learning Objectives

- Gain proficiency in data visualization libraries and Streamlit
- Understand the fundamentals of battle simulation algorithms
- Develop skills in user interface design and user experience
- ETL (Extract, Transform, Load) processes for handling datasets
- Neural network evolution using NEAT algorithm
