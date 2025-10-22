-- Stores base stats, types, and abilities
CREATE TABLE IF NOT EXISTS pokemon_fact (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE,
    hp INTEGER,
    attack INTEGER,
    defense INTEGER,
    special_attack INTEGER,
    special_defense INTEGER,
    speed INTEGER,
    type1 TEXT,
    type2 TEXT
);

-- Stores all moves and their properties
CREATE TABLE IF NOT EXISTS moves_dim (
    name TEXT PRIMARY KEY,
    power INTEGER,
    accuracy INTEGER,
    pp INTEGER,
    type TEXT,
    damage_class TEXT,  -- 'physical', 'special', or 'status'
    priority INTEGER
);

-- Stores Smogon competitive movesets
CREATE TABLE IF NOT EXISTS smogon_sets (
    pokemon_name TEXT PRIMARY KEY,
    ability TEXT,
    item TEXT,
    nature TEXT,
    move1 TEXT,
    move2 TEXT,
    move3 TEXT,
    move4 TEXT,
    ev_hp INTEGER DEFAULT 0,
    ev_attack INTEGER DEFAULT 0,
    ev_defense INTEGER DEFAULT 0,
    ev_special_attack INTEGER DEFAULT 0,
    ev_special_defense INTEGER DEFAULT 0,
    ev_speed INTEGER DEFAULT 0,
    usage_percent REAL,
    tier TEXT,
    FOREIGN KEY (pokemon_name) REFERENCES pokemon_fact(name)
);

-- Stores battle results
CREATE TABLE IF NOT EXISTS battle_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pokemon1_name TEXT,
    pokemon2_name TEXT,
    winner_name TEXT,
    turns INTEGER,
    pokemon1_hp_remaining INTEGER,
    pokemon2_hp_remaining INTEGER,
    battle_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (pokemon1_name) REFERENCES pokemon_fact(name),
    FOREIGN KEY (pokemon2_name) REFERENCES pokemon_fact(name),
    FOREIGN KEY (winner_name) REFERENCES pokemon_fact(name)
);

-- Stores Pokemon rankings/ELO ratings
CREATE TABLE IF NOT EXISTS pokemon_rankings (
    pokemon_name TEXT PRIMARY KEY,
    elo_rating INTEGER DEFAULT 1500,
    wins INTEGER DEFAULT 0,
    losses INTEGER DEFAULT 0,
    draws INTEGER DEFAULT 0,
    win_rate REAL DEFAULT 0.0,
    avg_turns_to_win REAL DEFAULT 0.0,
    last_updated DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (pokemon_name) REFERENCES pokemon_fact(name)
);

-- Stores the type effectiveness matrix
CREATE TABLE IF NOT EXISTS type_effectiveness (
    attacking_type TEXT,
    defending_type TEXT,
    multiplier REAL,
    PRIMARY KEY (attacking_type, defending_type)
);