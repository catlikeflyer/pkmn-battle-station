# Project Architecture for Pokemon Battle Ranking System

## Overview

Determine the strongest Pokemon through round-robin battles using:

- Base stats from PokeAPI
- Most used Smogon movesets
- NEAT algorithm for battle strategy evolution
- ELO ranking system

## Phase 1: Data Collection ✓

```
data_prep/
├── create_tables.py       # Initialize database
├── pokemon_fact.py        # Fetch ~900 Pokemon base stats
├── moves_dim.py          # Fetch all moves (937 moves)
├── smogon_sets.py        # Scrape top Smogon sets (TODO)
└── type_chart.py         # Populate type effectiveness (TODO)
```

## Phase 2: Core Battle Engine

```
core/
├── pokemon.py
│   └── Pokemon class with:
│       - Base stats (from pokemon_fact)
│       - Moveset (from smogon_sets)
│       - Current HP, status, stat modifiers
│       - Methods: take_damage(), use_move(), calculate_stats()
│
├── move.py
│   └── Move class with:
│       - Power, accuracy, type, priority
│       - execute() method for damage calculation
│
├── battle.py
│   └── Battle class with:
│       - Two Pokemon instances
│       - Turn-by-turn simulation
│       - Damage calculation (STAB, type effectiveness, crits)
│       - Winner determination
│
└── type_chart.py
    └── get_type_effectiveness(atk_type, def_types)
```

## Phase 3: NEAT Integration (Optional Enhancement)

```
ai/
├── neat_config.txt        # Population size, mutation rates, etc.
├── battle_ai.py
│   └── NeuralNetworkBrain:
│       - Inputs: Current HP %, opponent HP %, type matchup, move info
│       - Outputs: Move selection (4 moves + switch)
│       - Fitness: Win rate across battles
│
└── train_neat.py
    └── Evolve optimal battle strategies over generations
```

## Phase 4: Tournament System

```
tournament/
├── round_robin.py
│   └── run_tournament():
│       - Every Pokemon battles every other Pokemon
│       - ~400,000 battles (900 choose 2)
│       - Store results in battle_results table
│
├── elo_system.py
│   └── update_elo():
│       - K-factor based ELO rating
│       - Update pokemon_rankings table
│
└── analyze_results.py
    └── Generate rankings, visualizations, insights
```

## Phase 5: Streamlit Dashboard

```
streamlit_app.py           # Main Streamlit application
pages/
├── 1_Rankings.py          # Live rankings with filters
├── 2_Battle_Simulator.py  # Interactive 1v1 battles
├── 3_Tournament.py        # Run/view tournament results
├── 4_Analytics.py         # Deep dive statistics
└── 5_Type_Analysis.py     # Type effectiveness heatmaps

components/
├── pokemon_card.py        # Display Pokemon stats/moveset
├── battle_visualizer.py   # Animated turn-by-turn display
└── charts.py              # Reusable Plotly charts
```

## Database Schema

### pokemon_fact

- Base stats for all Pokemon
- Source: PokeAPI

### moves_dim

- All move properties
- Source: PokeAPI

### smogon_sets

- Most used competitive movesets
- Includes moves, ability, item, nature, EVs
- Source: Smogon usage stats

### battle_results

- Record of every battle fought
- Winner, turns, remaining HP
- Used for analytics

### pokemon_rankings

- ELO rating for each Pokemon
- Win/loss record
- Updated after each battle

## How NEAT Fits In

### Option A: NEAT for Battle AI (Recommended)

Instead of hardcoded battle logic, use NEAT to evolve optimal strategies:

- Each Pokemon gets a neural network "brain"
- Network decides which move to use based on battle state
- Fitness = win rate
- After evolution, use best networks for tournament

### Option B: Simple Battle Logic (Faster)

Use deterministic logic:

- Choose move with highest expected damage
- Consider type effectiveness and STAB
- Account for accuracy and priority
- No AI training needed

## Implementation Order

1. ✓ Setup database schema
2. Run pokemon_fact.py to cache Pokemon
3. Run moves_dim.py to cache moves
4. Create smogon_sets.py to fetch competitive sets
5. Build core battle engine (pokemon.py, battle.py)
6. Implement simple battle logic OR NEAT AI
7. Run round-robin tournament
8. Calculate ELO rankings
9. Visualize results

## Expected Runtime

- Data collection: ~30 minutes
- Round-robin (900 Pokemon): ~2-4 hours
  - Can parallelize battles
  - Can limit to top tiers (OU, UU, etc.)
- NEAT training (if used): Additional 1-8 hours

## Questions to Consider

1. **Which Pokemon to include?**

   - All 900+? or
   - Only OU/UU tiers?
   - Legendary restrictions?

2. **Battle rules?**

   - Level 100, full EVs
   - Items allowed?
   - Abilities active?

3. **NEAT or simple AI?**

   - NEAT: More interesting, slower
   - Simple: Faster, still valid results

4. **How to handle RNG?**
   - Run each matchup multiple times?
   - Average results?
